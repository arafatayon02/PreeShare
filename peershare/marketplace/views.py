from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import (
    Item, Review, Booking, Deposit,
    ChatMessage, Purchase, Payment
)
from .forms import (
    ItemForm, ReviewForm, BookingForm, ChatForm,
    CardPaymentForm, BkashPaymentForm
)

User = get_user_model()


# ── HOME ─────────────────────────────────────────────────
def home(request):
    query    = request.GET.get('q', '')
    category = request.GET.get('category', '')
    items    = Item.objects.filter(
                   is_available=True
               ).order_by('-created_at')

    if query:
        items = items.filter(title__icontains=query)
    if category:
        items = items.filter(category=category)

    return render(request, 'marketplace/home.html', {
        'items':    items,
        'query':    query,
        'category': category,
    })


# ── ADD ITEM ─────────────────────────────────────────────
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item       = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, '✅ Item posted!')
            return redirect('home')
    else:
        form = ItemForm()
    return render(
        request, 'marketplace/add_item.html',
        {'form': form}
    )


# ── ITEM DETAIL ───────────────────────────────────────────
@login_required
def item_detail(request, pk):
    item         = get_object_or_404(Item, pk=pk)
    reviews      = item.reviews.all().order_by('-created_at')
    review_form  = ReviewForm()
    booking_form = BookingForm()
    is_owner     = (request.user == item.owner)
    can_rent     = item.category in ['rent', 'both']
    can_buy      = item.category in ['sell', 'both']

    if request.method == 'POST':

        # ── BUY → go to payment page ──────────────────────
        if 'submit_buy' in request.POST and not is_owner:
            if item.is_available:
                request.session['pay_item_id'] = item.pk
                request.session['pay_type']    = 'buy'
                request.session['pay_amount']  = str(item.price)
                request.session['pay_days']    = None
                return redirect('payment')
            else:
                messages.error(
                    request,
                    '❌ This item is no longer available.'
                )

        # ── RENT → go to payment page ─────────────────────
        if 'submit_booking' in request.POST and not is_owner:
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                days  = booking_form.cleaned_data['days']
                total = round(float(item.price) * days, 2)
                request.session['pay_item_id'] = item.pk
                request.session['pay_type']    = 'rent'
                request.session['pay_amount']  = str(total)
                request.session['pay_days']    = days
                return redirect('payment')

        # ── REVIEW ────────────────────────────────────────
        if 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                r      = review_form.save(commit=False)
                r.item = item
                r.user = request.user
                r.save()
                messages.success(request, '⭐ Review submitted!')
                return redirect('item_detail', pk=pk)

    return render(request, 'marketplace/item_detail.html', {
        'item':          item,
        'reviews':       reviews,
        'review_form':   review_form,
        'booking_form':  booking_form,
        'is_owner':      is_owner,
        'can_rent':      can_rent,
        'can_buy':       can_buy,
    })


# ── PAYMENT PAGE ──────────────────────────────────────────
@login_required
def payment(request):
    item_id  = request.session.get('pay_item_id')
    pay_type = request.session.get('pay_type')
    amount   = request.session.get('pay_amount')
    days     = request.session.get('pay_days')

    if not item_id or not pay_type:
        messages.error(request, '❌ No payment session found.')
        return redirect('home')

    item = get_object_or_404(Item, pk=item_id)

    if not item.is_available:
        messages.error(
            request, '❌ This item is no longer available.'
        )
        return redirect('item_detail', pk=item_id)

    # For rent: advance = 50% of total
    advance = None
    remaining = None
    if pay_type == 'rent':
        advance   = round(float(amount) * 0.50, 2)
        remaining = round(float(amount) * 0.50, 2)

    card_form  = CardPaymentForm(prefix='card')
    bkash_form = BkashPaymentForm(prefix='bkash')

    if request.method == 'POST':
        method = request.POST.get('payment_method', '')

        # ── CASH ON DELIVERY ──────────────────────────────
        if method == 'cod' and pay_type == 'buy':
            payment_obj = Payment.objects.create(
                payer        = request.user,
                item         = item,
                payment_type = pay_type,
                method       = 'cod',
                amount       = amount,
                days         = days,
                status       = 'pending',
            )
            Purchase.objects.create(
                item       = item,
                buyer      = request.user,
                price_paid = amount,
                status     = 'pending',
            )
            item.is_available = False
            item.save()
            _clear_session(request)
            return redirect(
                'payment_success',
                payment_id=payment_obj.pk
            )

        # ── CARD ──────────────────────────────────────────
        elif method == 'card':
            card_form = CardPaymentForm(
                request.POST, prefix='card'
            )
            if card_form.is_valid():
                card_number = card_form.cleaned_data[
                    'card_number'
                ]
                card_last4  = card_number[-4:]
                pay_amount  = advance if pay_type == 'rent' \
                              else amount

                payment_obj = Payment.objects.create(
                    payer          = request.user,
                    item           = item,
                    payment_type   = pay_type,
                    method         = 'card',
                    amount         = amount,
                    advance_amount = advance or 0,
                    days           = days,
                    card_last4     = card_last4,
                    status         = 'completed',
                )
                _complete_order(
                    request, item, pay_type,
                    amount, advance, days
                )
                _clear_session(request)
                return redirect(
                    'payment_success',
                    payment_id=payment_obj.pk
                )

        # ── BKASH ─────────────────────────────────────────
        elif method == 'bkash':
            bkash_form = BkashPaymentForm(
                request.POST, prefix='bkash'
            )
            if bkash_form.is_valid():
                payment_obj = Payment.objects.create(
                    payer          = request.user,
                    item           = item,
                    payment_type   = pay_type,
                    method         = 'bkash',
                    amount         = amount,
                    advance_amount = advance or 0,
                    days           = days,
                    bkash_number   = bkash_form.cleaned_data[
                                         'bkash_number'
                                     ],
                    bkash_txn_id   = bkash_form.cleaned_data[
                                         'bkash_txn_id'
                                     ],
                    status         = 'completed',
                )
                _complete_order(
                    request, item, pay_type,
                    amount, advance, days
                )
                _clear_session(request)
                return redirect(
                    'payment_success',
                    payment_id=payment_obj.pk
                )
        else:
            messages.error(
                request,
                '⚠️ Please select a payment method.'
            )

    return render(request, 'marketplace/payment.html', {
        'item':       item,
        'pay_type':   pay_type,
        'amount':     amount,
        'days':       days,
        'advance':    advance,
        'remaining':  remaining,
        'card_form':  card_form,
        'bkash_form': bkash_form,
    })


def _complete_order(request, item, pay_type,
                    amount, advance, days):
    """Create purchase/booking record and mark item."""
    if pay_type == 'buy':
        Purchase.objects.create(
            item       = item,
            buyer      = request.user,
            price_paid = amount,
            status     = 'confirmed',
        )
        item.is_available = False
        item.save()
    elif pay_type == 'rent':
        booking = Booking.objects.create(
            item         = item,
            renter       = request.user,
            days         = days,
            advance_paid = advance or 0,
        )
        Deposit.objects.create(
            booking = booking,
            amount  = advance or 0,
        )


def _clear_session(request):
    """Remove payment keys from session."""
    for key in ['pay_item_id', 'pay_type',
                'pay_amount', 'pay_days']:
        request.session.pop(key, None)


# ── PAYMENT SUCCESS ───────────────────────────────────────
@login_required
def payment_success(request, payment_id):
    payment_obj = get_object_or_404(
        Payment, pk=payment_id, payer=request.user
    )
    return render(
        request,
        'marketplace/payment_success.html',
        {'payment': payment_obj}
    )


# ── CHAT ─────────────────────────────────────────────────
@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    if other_user == request.user:
        return redirect('home')

    msgs = (
        ChatMessage.objects.filter(
            sender=request.user, receiver=other_user
        ) |
        ChatMessage.objects.filter(
            sender=other_user, receiver=request.user
        )
    ).order_by('timestamp')

    form = ChatForm()
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            ChatMessage.objects.create(
                sender=request.user,
                receiver=other_user,
                message=form.cleaned_data['message']
            )
            return redirect('chat', user_id=user_id)

    return render(request, 'marketplace/chat.html', {
        'other_user': other_user,
        'msgs':       msgs,
        'form':       form,
    })
# ── DELETE ITEM ───────────────────────────────────────────
@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Only the owner can delete
    if request.user != item.owner:
        messages.error(
            request,
            '❌ You are not allowed to delete this item.'
        )
        return redirect('home')

    if request.method == 'POST':
        item_title = item.title
        item.delete()
        messages.success(
            request,
            f'🗑️ "{item_title}" has been deleted successfully.'
        )
        return redirect('dashboard_items')

    # GET → show confirmation page
    return render(
        request,
        'marketplace/delete_item.html',
        {'item': item}
    )