from django.db import models
from django.utils import timezone

class Membership(models.Model):
    MEMBERSHIP_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    
    membership_type = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_TYPES,
        default='basic'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='inactive'
    )
    
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.membership_type}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_active(self):
        return self.status == 'active' and (
            self.end_date is None or self.end_date > timezone.now()
        )
    
    @property
    def days_remaining(self):
        if self.end_date and self.status == 'active':
            remaining = self.end_date - timezone.now()
            return max(0, remaining.days)
        return 0
    
    def save(self, *args, **kwargs):
        if not self.end_date and self.status == 'active':
            self.end_date = self.start_date + timezone.timedelta(days=365)
        super().save(*args, **kwargs)
