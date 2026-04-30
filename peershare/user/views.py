from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm
from marketplace.models import Item, Booking, Review

User = get_user_model()


@login_required
def dashboard(request):
    profile     = request.user.profile
    my_items    = Item.objects.filter(owner=request.user).order_by('-created_at')
    my_bookings = Booking.objects.filter(renter=request.user).order_by('-booked_at')
    my_reviews  = Review.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'user/dashboard.html', {
        'profile':     profile,
        'my_items':    my_items,
        'my_bookings': my_bookings,
        'my_reviews':  my_reviews,
    })


@login_required
def my_profile(request):
    profile = request.user.profile
    return render(request, 'user/my_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/edit_profile.html', {'form': form})


def public_profile(request, username):
    viewed_user = get_object_or_404(User, username=username)
    profile     = get_object_or_404(Profile, user=viewed_user)
    user_items  = Item.objects.filter(owner=viewed_user).order_by('-created_at')

    return render(request, 'user/public_profile.html', {
        'viewed_user': viewed_user,
        'profile':     profile,
        'user_items':  user_items,
    })


@login_required
def all_users(request):
    search   = request.GET.get('q', '')
    profiles = Profile.objects.select_related('user').all()

    if search:
        profiles = profiles.filter(user__username__icontains=search)

    return render(request, 'user/all_users.html', {
        'profiles': profiles,
        'search':   search,
    })