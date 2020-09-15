from django.urls import path
from .views import *


urlpatterns = [
    path('list_expense_by_category/', list_expense_by_category, name="list_expense_by_category"),
    path('list_expense_by_date/', list_expense_by_date, name="list_expense_by_date"),
    path('create_expense/', create_expense, name="create_expense"),
    path('delete_expense/', delete_expense, name="delete_expense"),
    path('update_expense/', update_expense, name="update_expense"),
    path('get_expense/', get_expense, name="get_expense")
]