from django.urls import path
from apps.news.views import *


urlpatterns = [
    # Новости и форма создания
    path('', news_list, name='news_posts'),
    path('new/', NewsPostCreateView.as_view(), name='news_new'),

    # Детали поста и лайки
    path('post/<int:pk>/', NewsPostDetailView.as_view(), name='post_detail'),
    path('like/<int:pk>/', like_view, name='like_post'),
    
    # Комментарии
    path('news/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('delete_comment/<int:pk>/', comment_delete, name='comment_delete'),
    path('edit_comment/<int:pk>/', comment_edit, name='comment_edit'),
]
