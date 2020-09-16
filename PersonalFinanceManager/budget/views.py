from .forms import *
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Sum
# Create your views here.


def unfold_budget(budgets):
    result = list()
    for budget in budgets:
        temp = model_to_dict(budget)
        temp['category'] = model_to_dict(budget.category)
        temp['category']["category"] = model_to_dict(Category.objects.get(id=temp['category']["category"]))
        result.append(temp)
    return result


@api_view(("get",))
def list_budget(request):
    budgets = Budget.objects.all()

    result = unfold_budget(budgets)

    return JsonResponse({"result": result, "status": "success"})


@api_view(("get",))
def list_budget_by_category(request):
    categorys = Category.objects.all()

    result = dict()
    for category in categorys:
        sub_categorys = SubCategory.objects.filter(category=category)
        result[str(category)] = Budget.objects.filter(category__in=sub_categorys).aggregate(Sum("amount"))

    return JsonResponse({"result": result, "status": "success"})


@api_view(("post",))
def list_budget_by_sub_category(request):
    existed_category = Category.objects.filter(id=request.data['id'])

    if existed_category:
        category = existed_category.first()
        sub_categorys = SubCategory.objects.filter(category=category)
        print(sub_categorys)
        result = dict()
        for sub_category in sub_categorys:
            result[str(sub_category)] = Budget.objects.filter(category=sub_category).aggregate(Sum("amount"))
        return JsonResponse({"result": result, "status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def create_budget(request):
    request.data["category"] = SubCategory.objects.get(id=request.data['category'])

    budget_form = BudgetForm(request.data)

    if budget_form.is_valid():
        budget_form.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def delete_budget(request):
    existed_budget = Budget.objects.filter(id=request.data['id'])

    if existed_budget:
        result = existed_budget.first()
        result.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def update_budget(request):
    request.data["category"] = SubCategory.objects.get(id=request.data['category'])
    budget_form = BudgetForm(request.data)

    if budget_form.is_valid():
        Budget.objects.filter(id=request.data['id']).update(**budget_form.cleaned_data)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def get_budget(request):
    existed_budget = Budget.objects.filter(id=request.data['id'])

    if existed_budget:
        result = model_to_dict(existed_budget.first())
        return JsonResponse({"result": result, "status": "success"})
    return JsonResponse({"status": "failure"})
