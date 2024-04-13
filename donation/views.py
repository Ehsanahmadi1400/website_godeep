from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View

from donation.forms import DonationForm
from donation.models import Donation
from utils.zarinpal import zpal_request_handler


class DonationView(View):
    template_name = 'donation/donation.html'
    form_class = DonationForm

    def get_context_data(self):
        donations = Donation.objects.filter(is_enable=True)
        return dict(donations=donations)

    def get(self, request, *args, **kwargs):
        return render(request, 'donation/donation.html', self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            payment_link, authority = zpal_request_handler(
                settings.ZARINPAL['merchant_id'], form.cleaned_data['amount'],
                'Tea', 'ehsan.btg@gmail.com', None,
                settings.ZARINPAL['gateway_callback_url']
            )

            if payment_link is not None:
                return redirect(payment_link)
        print('*** form is not valid')
        return render(request, self.template_name, {'donations': form})
