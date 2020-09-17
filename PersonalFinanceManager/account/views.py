from .forms import *
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.forms.models import model_to_dict
import pandas as pd
from expense.views import unfold_expense
from income.views import unfold_income
# Create your views here.


@api_view(("post",))
def list_transaction(request):
    account = Account.objects.get(id=request.data['id'])

    expenses = account.expense_set.all()
    incomes = account.income_set.all()

    result = {"expense": unfold_expense(expenses), "income": unfold_income(incomes)}

    return JsonResponse({"result": result, "status": "success"})


@api_view(("get",))
def list_account(request):
    accounts = Account.objects.all().values()

    result = list(accounts)

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


@api_view(("post",))
def get_account(request):
    existed_category = Account.objects.filter(id=request.data['id'])

    if existed_category:
        result = model_to_dict(existed_category.first())
        return JsonResponse({"result": result, "status": "success"})
    return JsonResponse({"status": "failure"})

@api_view(("post","get"))
def import_csv(request):
    data = request.FILES["data"]
    if data:
        df = pd.read_csv(data)
    return JsonResponse({"status": "failure"})
