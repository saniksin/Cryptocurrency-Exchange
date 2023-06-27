from django.urls import path
from apps.exchange import views


urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('aml/', views.AmlView.as_view(), name="aml"),
    path('rules/', views.RulesView.as_view(), name="rules"),
    path('notice/', views.NoticeView.as_view(), name="notice")
]