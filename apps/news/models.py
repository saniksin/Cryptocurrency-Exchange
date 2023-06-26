from django.db import models
from apps.users.models import User


class NewsPost(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField("Фото", upload_to="posts/images/")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField("Активный", default=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Новостной пост"
        verbose_name_plural = "Новостные посты"

    def total_likes(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name="post_comments")
    text = models.CharField("Комментарий", max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
    
    def __str__(self):
        return f"{self.text}"