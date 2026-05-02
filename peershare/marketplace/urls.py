from django.urls import path
from . import views

urlpatterns = [
    path('',                    views.home,        name='home'),
    path('add/',                views.add_item,    name='add_item'),
    path('item/<int:pk>/',      views.item_detail, name='item_detail'),
    path('chat/<int:user_id>/', views.chat,        name='chat'),
]