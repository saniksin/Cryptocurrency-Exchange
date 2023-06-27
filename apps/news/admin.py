from django.contrib import admin
from apps.news.models import NewsPost, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0 


class NewsPostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__email')
    ordering = ('-created_at',)


admin.site.register(NewsPost, NewsPostAdmin)

