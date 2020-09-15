from .views import *
from django.urls import path


urlpatterns = [
    path('list_category/', list_category, name="list_category"),
    path('list_sub_category/', list_sub_category, name="list_sub_category"),
    path('create_category/', create_category, name="create_category"),
    path('create_sub_category/', create_sub_category, name="create_sub_category"),
    path('delete_category/', delete_category, name="delete_category"),
    path('delete_sub_category/', delete_sub_category, name="delete_sub_category"),
    path('update_category/', update_category, name="update_category"),
    path('update_sub_category/', update_sub_category, name="update_sub_category"),
    path('get_category/', get_category, name="get_category"),
    path('get_sub_category/', get_sub_category, name="get_sub_category"),
]