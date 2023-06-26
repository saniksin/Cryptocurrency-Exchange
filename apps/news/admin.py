from django.contrib import admin
from apps.news.models import NewsPost


class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__email')
    ordering = ('-created_at',)

    
    class Meta:
        verbose_name = 'Новостной пост'
        verbose_name_plural = 'Новостные посты'

admin.site.register(NewsPost, NewsPostAdmin)
