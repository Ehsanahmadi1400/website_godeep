from django import forms


class DonationForm(forms.Form):
    amount = forms.IntegerField()