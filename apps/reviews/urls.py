from django.urls import path
from apps.reviews import views


urlpatterns = [
    path('', views.ReviewListView.as_view(), name='reviews'),

    # Действия с отзывом
    path('add/', views.add_review, name='add_review'),
    path('delete_review/<int:pk>/', views.review_delete, name='review_delete'),
    path('edit_review/<int:pk>/', views.review_edit, name='review_edit'),
]