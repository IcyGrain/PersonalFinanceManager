from .views import *
from django.urls import path


urlpatterns = [
    path('list_account/', list_account, name="list_account"),
    path('create_account/', create_account, name="create_account"),
    path('delete_account/', delete_account, name="delete_account"),
    path('update_account/', update_account, name="update_account"),
    path('import_csv/', import_csv, name="import_csv"),
]