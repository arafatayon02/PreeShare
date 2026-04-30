from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Item, Review, Booking, Deposit, ChatMessage
from .forms import ItemForm, ReviewForm, BookingForm, ChatForm

User = get_user_model()


def home(request):
    query    = request.GET.get('q', '')
    category = request.GET.get('category', '')
    items    = Item.objects.all().order_by('-created_at')

    if query:
        items = items.filter(title__icontains=query)
    if category:
        items = items.filter(category=category)

    return render(request, 'marketplace/home.html', {
        'items':    items,
        'query':    query,
        'category': category,
    })


@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item       = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, '✅ Item posted successfully!')
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'marketplace/add_item.html', {'form': form})


@login_required
def item_detail(request, pk):
    item         = get_object_or_404(Item, pk=pk)
    reviews      = item.reviews.all().order_by('-created_at')
    review_form  = ReviewForm()
    booking_form = BookingForm()

    if request.method == 'POST':

        if 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                r      = review_form.save(commit=False)
                r.item = item
                r.user = request.user
                r.save()
                messages.success(request, '⭐ Review submitted!')
                return redirect('item_detail', pk=pk)

        if 'submit_booking' in request.POST:
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                b        = booking_form.save(commit=False)
                b.item   = item
                b.renter = request.user
                b.save()
                Deposit.objects.create(
                    booking=b,
                    amount=b.total_price * 10 / 100
                )
                messages.success(request, f'📅 Booked for {b.days} days! Total: ৳{b.total_price}')
                return redirect('dashboard')

    return render(request, 'marketplace/item_detail.html', {
        'item':         item,
        'reviews':      reviews,
        'review_form':  review_form,
        'booking_form': booking_form,
    })


@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)

    if other_user == request.user:
        return redirect('home')

    msgs = (
        ChatMessage.objects.filter(sender=request.user, receiver=other_user) |
        ChatMessage.objects.filter(sender=other_user,   receiver=request.user)
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