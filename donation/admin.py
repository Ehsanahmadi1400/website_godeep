from django.contrib import admin
from django.contrib.admin import register
from donation.models import Donation


@register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_enable']
