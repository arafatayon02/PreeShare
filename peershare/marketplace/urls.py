from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_item, name='add_item'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('payment/', views.payment, name='payment'),
    path('payment/success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('chat/<int:user_id>/', views.chat, name='chat'),
]