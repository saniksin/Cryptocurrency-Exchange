from django.urls import path

from apps.exchange import views


urlpatterns = [
    # Главная
    path('', views.IndexView.as_view(), name="index"),

    # Основные правила
    path('aml/', views.AmlView.as_view(), name="aml"),
    path('rules/', views.RulesView.as_view(), name="rules"),
    path('notice/', views.NoticeView.as_view(), name="notice"),

    # Обмен и статус транзакции
    path('transaction/confirm/', views.confirm, name='confirm'),
    path('transaction/info/<str:unique_transaction_number>/', views.transaction_info, name='transaction_info'),
    path('transaction/mark_paid/<str:unique_transaction_number>/', views.mark_transaction_as_paid, name='mark_paid'),
    path('transaction/cancel/<str:unique_transaction_number>/', views.cancel_transaction, name='cancel_transaction'),
]