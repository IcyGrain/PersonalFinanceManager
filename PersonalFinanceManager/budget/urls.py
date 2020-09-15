from .views import *
from django.urls import path


urlpatterns = [
    path('list_budget_by_category/', list_budget_by_category, name="list_budget_by_category"),
    path('list_budget_by_sub_category/', list_budget_by_sub_category, name="list_budget_by_sub_category"),
    path('create_budget/', create_budget, name="create_budget"),
    path('delete_budget/', delete_budget, name="delete_budget"),
    path('update_budget/', update_budget, name="update_budget"),
    path('get_budget/', get_budget, name="get_budget")
]