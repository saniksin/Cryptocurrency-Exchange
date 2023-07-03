from django import forms

from apps.news.models import NewsPost, Comment


# форма нового поста
class NewsPostForm(forms.ModelForm):

    class Meta:
        model = NewsPost
        fields = ['title', 'description', 'image']


# форма комментария
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

