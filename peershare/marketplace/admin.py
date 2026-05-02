from django.contrib import admin
from .models import Item, Review, Booking, Deposit, ChatMessage


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'category', 'price', 'created_at']
    list_filter   = ['category']
    search_fields = ['title', 'owner__username']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'rating', 'created_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['renter', 'item', 'days', 'total_price', 'booked_at']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'returned']


@admin.register(ChatMessage)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp']