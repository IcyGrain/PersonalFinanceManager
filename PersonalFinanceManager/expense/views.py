from datetime import timedelta

from .forms import *
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Sum
from budget.models import *


# Create your views here.


def unfold_expense(expenses):
    result = list()
    for expense in expenses:
        temp = model_to_dict(expense)
        temp['category'] = model_to_dict(expense.category)
        temp['category']["category"] = model_to_dict(Category.objects.get(id=temp['category']["category"]))
        temp['account'] = model_to_dict(expense.account)
        result.append(temp)
    return result


@api_view(("get",))
def list_expense(request):
    expenses = Expense.objects.all()

    result = unfold_expense(expenses)

    return JsonResponse({"result": result, "status": "success"})


@api_view(("get",))
def list_expense_by_category(request):
    categorys = Category.objects.all()

    result = dict()
    for category in categorys:
        sub_categorys = SubCategory.objects.filter(category=category)
        result[str(category)] = [{str(sub_category): list(Expense.objects.filter(category=sub_category).values())}
                                 for sub_category in sub_categorys]

    return JsonResponse({"result": result, "status": "success"})


@api_view(("get",))
def list_expense_by_date(request):
    dates = Expense.objects.values_list("date", flat=True).distinct()

    result = {str(date): list(Expense.objects.filter(date=date).select_related("account").values()) for date in dates}

    return JsonResponse({"result": result, "status": "success"})


# @api_view(("get",))
# def list_expense_by_date(request):
#     dates = Expense.objects.values_list("date", flat=True).distinct()
#     result = dict()
#     for date in dates:
#         expenses = Expense.objects.filter(date=date)
#         for expense in expenses:
#             expense.account = model_to_dict(expense.account)
#             expense.category = model_to_dict(expense.category)
#         result[str(date)] = list(expenses.values())
#
#     return JsonResponse({"result": result, "status": "success"})


@api_view(("post",))
def create_expense(request):
    request.data["category"] = SubCategory.objects.get(id=request.data['category'])
    request.data["account"] = Account.objects.get(id=request.data['account'])
    expense_form = ExpenseForm(request.data)

    if expense_form.is_valid():

        existed_budget = Budget.objects.filter(category=request.data['category'], start_date__lte=request.data["date"],
                                               end_date__gte=request.data["date"])
        if existed_budget:
            budget = existed_budget.first()
        else:
            budget = Budget.objects.create(amount=0, category=request.data['category'], budget_type="fixed",
                                  start_date=timezone.now().strftime("%Y-%m-%d"),
                                  end_date=(timezone.now() + timedelta(days=30)).strftime("%Y-%m-%d"))

        request.data["account"].balance -= expense_form.cleaned_data["amount"]
        budget.amount -= expense_form.cleaned_data["amount"]

        budget.save()
        request.data["account"].save()
        expense_form.save()
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "failure"})


@api_view(("post",))
def delete_expense(request):
    existed_expense = Expense.objects.filter(id=request.data['id'])

    if existed_expense:
        expense = existed_expense.first()

        existed_budget = Budget.objects.filter(category=expense.category, start_date__lte=expense.date,
                                               end_date__gte=expense.date)
        if existed_budget:
            budget = existed_budget.first()
            budget.amount += expense.amount
            budget.save()
        expense.account.balance += expense.amount
        expense.account.save()
        expense.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def update_expense(request):
    request.data["category"] = SubCategory.objects.get(id=request.data['category'])
    request.data["account"] = Account.objects.get(id=request.data['account'])

    expense_form = ExpenseForm(request.data)
    old_amount = Expense.objects.get(id=request.data["id"]).amount
    if expense_form.is_valid():

        existed_budget = Budget.objects.filter(category=request.data['category'], start_date__lte=request.data["date"],
                                               end_date__gte=request.data["date"])
        if existed_budget:
            budget = existed_budget.first()
            budget.amount -= expense_form.cleaned_data['amount'] - old_amount
            budget.save()

        request.data["account"].balance -= expense_form.cleaned_data["amount"] - old_amount
        request.data["account"].save()
        Expense.objects.filter(id=request.data['id']).update(**expense_form.cleaned_data)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def get_expense(request):
    existed_expense = Expense.objects.filter(id=request.data['id'])

    if existed_expense:
        result = unfold_expense(existed_expense)
        return JsonResponse({"result": result, "status": "success"})
    return JsonResponse({"status": "failure"})
