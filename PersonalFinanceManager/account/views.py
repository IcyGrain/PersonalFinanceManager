from .forms import *
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.forms.models import model_to_dict
import pandas as pd
# Create your views here.


@api_view(("get",))
def list_account(request):
    category = Account.objects.all().values()

    result = list(category)

    return JsonResponse({"result": result, "status": "success"})


@api_view(("post",))
def create_account(request):
    account_form = AccountForm(request.data)

    if account_form.is_valid():
        account_form.save()
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "failure"})


@api_view(("post",))
def delete_account(request):
    existed_account = Account.objects.filter(id=request.data['id'])

    if existed_account:
        result = existed_account.first()
        result.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def update_account(request):
    account_form = AccountForm(request.data)

    if account_form.is_valid():
        Account.objects.filter(id=request.data['id']).update(**account_form.cleaned_data)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post","get"))
def import_csv(request):
    data = request.FILES["data"]
    if data:
        df = pd.read_csv(data)
    return JsonResponse({"status": "failure"})
