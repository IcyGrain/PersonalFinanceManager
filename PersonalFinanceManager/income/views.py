from .forms import *
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.forms.models import model_to_dict
# Create your views here.


def unfold_income(incomes):
    result = list()
    for income in incomes:
        temp = model_to_dict(income)
        temp['account'] = model_to_dict(income.account)
        result.append(temp)
    return result


@api_view(("get",))
def list_income(request):
    incomes = Income.objects.all()

    result = unfold_income(incomes)

    return JsonResponse({"result": result, "status": "success"})


@api_view(("get",))
def list_income_by_source(request):
    sources = Income.objects.values_list("source", flat=True).distinct()

    result = {source:list(Income.objects.filter(source=source).values()) for source in sources}

    return JsonResponse({"result": result, "status": "success"})


@api_view(("get",))
def list_income_by_date(request):
    dates = Income.objects.values_list("date", flat=True).distinct()

    result = {str(date): list(Income.objects.filter(date=date).values()) for date in dates}

    return JsonResponse({"result": result, "status": "success"})


@api_view(("post",))
def create_income(request):
    request.data["account"] = Account.objects.get(id=request.data['account'])

    income_form = IncomeForm(request.data)

    if income_form.is_valid():
        income_form.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def delete_income(request):
    existed_income = Income.objects.filter(id=request.data['id'])

    if existed_income:
        result = existed_income.first()
        result.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def update_income(request):
    request.data["account"] = Account.objects.get(id=request.data['account'])
    income_form = IncomeForm(request.data)

    if income_form.is_valid():
        Income.objects.filter(id=request.data['id']).update(**income_form.cleaned_data)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def get_income(request):
    existed_income = Income.objects.filter(id=request.data['id'])

    if existed_income:
        result = model_to_dict(existed_income.first())
        return JsonResponse({"result": result, "status": "success"})
    return JsonResponse({"status": "failure"})
