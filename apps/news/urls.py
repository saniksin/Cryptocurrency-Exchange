from django.urls import path

from apps.news import views


urlpatterns = [
    # Новости и форма создания
    path('', views.news_list, name='news_posts'),
    path('add/', views.NewsPostCreateView.as_view(), name='news_new'),

    # Детали поста и лайки
    path('post/<int:pk>/', views.NewsPostDetailView.as_view(), name='post_detail'),
    path('post/like/<int:pk>/', views.like_view, name='like_post'),
    path('post/delete/<int:pk>/', views.NewsDeleteView.as_view(), name='post_delete'),
    path('post/edit/<int:pk>/', views.NewsUpdateView.as_view(), name='post_update'),
    
    # Комментарии
    path('add/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('delete_comment/<int:pk>/', views.comment_delete, name='comment_delete'),
    path('edit_comment/<int:pk>/', views.comment_edit, name='comment_edit'),
]
