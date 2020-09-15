from .views import *
from django.urls import path


urlpatterns = [
    path('list_income_by_source/', list_income_by_source, name="list_income_by_source"),
    path('list_income_by_date/', list_income_by_date, name="list_income_by_date"),
    path('create_income/', create_income, name="create_income"),
    path('delete_income/', delete_income, name="delete_income"),
    path('update_income/', update_income, name="update_income"),
]