from django import forms


class DonationForm(forms.Form):
    price = forms.IntegerField()
