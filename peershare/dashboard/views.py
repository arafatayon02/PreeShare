from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from marketplace.models import (
    Item, Purchase, Booking, ChatMessage, Review
)
from user.models import Profile

User = get_user_model()


@login_required
def dashboard_home(request):
    profile = request.user.profile
    my_items = Item.objects.filter(
        owner=request.user
    ).order_by('-created_at')
    purchases = Purchase.objects.filter(
        buyer=request.user
    ).order_by('-purchased_at')
    bookings = Booking.objects.filter(
        renter=request.user
    ).order_by('-booked_at')
    reviews = Review.objects.filter(
        user=request.user
    ).order_by('-created_at')

    sent = ChatMessage.objects.filter(
        sender=request.user
    ).values_list('receiver', flat=True)
    received = ChatMessage.objects.filter(
        receiver=request.user
    ).values_list('sender', flat=True)
    chat_users = User.objects.filter(
        id__in=set(list(sent) + list(received))
    )

    total_spent = sum(p.price_paid for p in purchases)
    total_rent = sum(b.total_price for b in bookings)

    return render(request, 'dashboard/home.html', {
        'profile': profile,
        'my_items': my_items,
        'purchases': purchases,
        'bookings': bookings,
        'reviews': reviews,
        'chat_users': chat_users,
        'total_spent': total_spent,
        'total_rent': total_rent,
    })


@login_required
def dashboard_purchases(request):
    purchases = Purchase.objects.filter(
        buyer=request.user
    ).order_by('-purchased_at')
    return render(request, 'dashboard/purchases.html', {
        'purchases': purchases
    })


@login_required
def dashboard_bookings(request):
    bookings = Booking.objects.filter(
        renter=request.user
    ).order_by('-booked_at')
    return render(request, 'dashboard/bookings.html', {
        'bookings': bookings
    })


@login_required
def dashboard_rentals(request):
    my_item_ids = Item.objects.filter(
        owner=request.user
    ).values_list('id', flat=True)
    incoming = Booking.objects.filter(
        item_id__in=my_item_ids
    ).order_by('-booked_at')
    return render(request, 'dashboard/rentals.html', {
        'incoming': incoming
    })


@login_required
def dashboard_chats(request):
    sent = ChatMessage.objects.filter(
        sender=request.user
    ).values_list('receiver', flat=True)
    received = ChatMessage.objects.filter(
        receiver=request.user
    ).values_list('sender', flat=True)
    user_ids = set(list(sent) + list(received))
    chat_users = User.objects.filter(id__in=user_ids)

    conversations = []
    for u in chat_users:
        last_msg = (
                ChatMessage.objects.filter(
                    sender=request.user, receiver=u
                ) |
                ChatMessage.objects.filter(
                    sender=u, receiver=request.user
                )
        ).order_by('timestamp').last()
        conversations.append({
            'user': u,
            'last_msg': last_msg,
        })

    return render(request, 'dashboard/chats.html', {
        'conversations': conversations
    })


@login_required
def dashboard_items(request):
    my_items = Item.objects.filter(
        owner=request.user
    ).order_by('-created_at')
    return render(request, 'dashboard/items.html', {
        'my_items': my_items
    })

