from django.db import models
from django.conf import settings


class Profile(models.Model):
    UNIVERSITY_CHOICES = [
        ('farmgate', 'University of Asia Pacific'),
        ('dhaka', 'University of Dhaka'),
        ('buet',  'BUET'),
        ('nsu',   'North South University'),
        ('bracu', 'BRAC University'),
        ('cuet',  'CUET'),
        ('ruet',  'RUET'),
        ('other', 'Other'),
    ]


    user        = models.OneToOneField(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name='profile'
                  )
    bio         = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(
                    upload_to='profiles/',
                    blank=True, null=True
                  )
    university  = models.CharField(
                    max_length=100,
                    choices=UNIVERSITY_CHOICES,
                    blank=True
                  )
    phone       = models.CharField(max_length=20, blank=True)
    location    = models.CharField(max_length=100, blank=True)
    joined_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_total_items(self):
        return self.user.items.count()

    def get_average_rating(self):
        from marketplace.models import Review
        reviews = Review.objects.filter(item__owner=self.user)
        if reviews.exists():
            return round(
                sum(r.rating for r in reviews) / reviews.count(), 1
            )
        return None