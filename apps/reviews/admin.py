from django.contrib import admin
from apps.reviews.models import Review


# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at') 
    search_fields = ('user__username', 'text') 
    ordering = ('-created_at',)  


admin.site.register(Review, ReviewAdmin)

