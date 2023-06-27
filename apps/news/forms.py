from django import forms
from django.contrib import admin
from apps.news.models import NewsPost, Comment


class NewsPostForm(forms.ModelForm):

    class Meta:
        model = NewsPost
        fields = ['title', 'description', 'image']


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'maxlength': 200,
            'placeholder': 'Ваш комментарий... (максимум 200 символов)'
        })
    )

    class Meta:
        model = Comment
        fields = ('text',)


