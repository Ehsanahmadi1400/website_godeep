from django.urls import path
from donation.views import DonationView


urlpatterns = [
    path('payment/', DonationView.as_view(), name='donation')

]
