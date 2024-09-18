from django import forms
from . import models

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        exclude = ['user', 'product', 'created_at']