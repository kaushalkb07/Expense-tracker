from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # URL for signup
    path('expense_home/', views.expense_home, name='expense_home'),
    path('addexpense/', views.addexpense, name='addexpense'),
    path('expense/<str:slug>', views.view_expense, name='view_expense'),
    path('expense/edit/<slug:slug>/', views.edit_expense, name='edit_expense'),
    path('expense/delete/<slug:slug>/', views.delete_expense, name='delete_expense'),
    path('search/', views.search_expense, name='search_expense'),
    path('exchange_rates/', views.exchange_rates_view, name='exchange_rates'),
    path('currency_converter/', views.currency_converter_view, name='currency_converter'),
    path('export/csv/', views.export_expenses_csv, name='export_expenses_csv'),
    path('export/excel/', views.export_expenses_excel, name='export_expenses_excel'),
]