from django import forms
from store.models import *

class CheckoutForm(forms.Form):
    name= forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control'}))

    phone= forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control'}))

    email= forms.EmailField(widget=forms.TextInput(
        attrs={
            'class':'form-control'}))

    address= forms.CharField(widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'col':30,
            'row':4
        }))

    order_note= forms.CharField(widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'col':30,
            'row':4
        }))

PAYMENT_METHOD=(
    ('Cash on delivery', 'Cash on delivery'),
    ('SSL Commerce', 'SSL Commerce'),
)


class PaymentmethodForm(forms.ModelForm):
    payment_option=forms.ChoiceField(widget=forms.RadioSelect(
        attrs={
            'class':'collapsed'}),choices=PAYMENT_METHOD)

    class Meta:
        model = Order
        fields = ['payment_option']
