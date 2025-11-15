from django.urls import path
from . import views

app_name = 'spese_app'

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('nuova/', views.expense_create, name='expense_create'),
    path('report-mensile/', views.monthly_report, name='monthly_report'),
]