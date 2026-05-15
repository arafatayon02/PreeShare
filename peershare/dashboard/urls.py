from django.urls import path
from . import views

urlpatterns = [
    path('',           views.dashboard_home,      name='dashboard'),
    path('purchases/', views.dashboard_purchases,  name='dashboard_purchases'),
    path('bookings/',  views.dashboard_bookings,   name='dashboard_bookings'),
    path('rentals/',   views.dashboard_rentals,    name='dashboard_rentals'),
    path('chats/',     views.dashboard_chats,      name='dashboard_chats'),
    path('items/',     views.dashboard_items,      name='dashboard_items'),
]
