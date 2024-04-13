from django.shortcuts import render
from django.views import View

from donation.models import Donation


class DonationView(View):

    def get_context_data(self):
        donations = Donation.objects.filter(is_enable=True)
        return dict(donations=donations)

    def get(self, request, *args, **kwargs):
        return render(request, 'donation/donation.html', self.get_context_data())
