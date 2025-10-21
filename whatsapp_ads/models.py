from django.db import models
from django.conf import settings

MEMBERSHIP_CHOICES = [
    ('normal', 'Normal'),
    ('vip', 'VIP'),
]

class WhatsAppUser(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='normal')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.membership_type})"
