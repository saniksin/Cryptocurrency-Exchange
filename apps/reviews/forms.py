from django import forms
from apps.reviews.models import Review


class ReviewForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'maxlength': 50,
            'placeholder': 'Ваш комментарий... (максимум 50 символов)'
        })
    )

    class Meta:
        model = Review
        fields = ('text',)

