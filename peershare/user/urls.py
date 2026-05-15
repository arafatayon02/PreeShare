from django.urls import path
from . import views

urlpatterns = [
    path('profile/',         views.my_profile,    name='my_profile'),
    path('profile/edit/',    views.edit_profile,  name='edit_profile'),
    path('all/',             views.all_users,     name='all_users'),
    path('<str:username>/',  views.public_profile, name='public_profile'),
]
