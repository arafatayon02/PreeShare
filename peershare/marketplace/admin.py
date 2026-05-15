from django.contrib import admin
from .models import (
    Item, Purchase, Booking,
    Deposit, Review, ChatMessage, Payment
)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'category',
                     'price', 'is_available', 'created_at']
    list_filter   = ['category', 'is_available']
    search_fields = ['title', 'owner__username']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payer', 'item', 'payment_type',
                    'amount', 'card_last4', 'status', 'paid_at']
    list_filter  = ['payment_type', 'status']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'item', 'price_paid',
                    'status', 'purchased_at']
    list_filter  = ['status']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['renter', 'item', 'days',
                    'total_price', 'status', 'booked_at']
    list_filter  = ['status']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'returned']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'rating', 'created_at']


@admin.register(ChatMessage)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp']