from django.urls import path
from donation.views import DonationView, VerifyView


urlpatterns = [
    path('payment/', DonationView.as_view(), name='donation'),
    path('verify/', VerifyView.as_view(), name='verify')

]
