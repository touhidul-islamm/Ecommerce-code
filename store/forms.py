from django import forms
from store.models import *

class ProductReviewForm(forms.ModelForm):
    RATING=(
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    rating=forms.ChoiceField(widget=forms.RadioSelect(
        attrs={ }), choices=RATING)
    
    image=forms.ImageField(required=False)
    review=forms.CharField(widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'placeholder':'comment',
            'row':2
        }))

    class Meta:
        model=ProductReview
        fields=['rating', 'review', 'image']

