from .forms import *
from rest_framework.decorators import api_view
from django.http import JsonResponse, QueryDict
from django.forms.models import model_to_dict


@api_view(("get",))
def list_category(request):
    category = Category.objects.all().values()

    result = list(category)

    return JsonResponse({"result": result, "status": "success"})


@api_view(("post",))
def list_sub_category(request):
    category = request.data['id']
    sub_categorys = SubCategory.objects.filter(category=category).values()

    result = list(sub_categorys)
    return JsonResponse({"result": result, "status": "success"})


@api_view(("post",))
def create_category(request):
    category_form = CategoryForm(request.data)

    if category_form.is_valid():
        category_form.save()
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "failure"})


@api_view(("post",))
def create_sub_category(request):
    if isinstance(request.data, QueryDict):
        request.data = request.data.dict()
    request.data["category"] = Category.objects.get(id=request.data['category'])

    sub_category_form = SubCategoryForm(request.data)

    if sub_category_form.is_valid():
        sub_category_form.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def delete_category(request):
    existed_category = Category.objects.filter(id=request.data['id'])

    if existed_category:
        result = existed_category.first()
        result.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def delete_sub_category(request):
    existed_category = SubCategory.objects.filter(id=request.data['id'])

    if existed_category:
        result = existed_category.first()
        result.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def update_category(request):
    category_form = CategoryForm(request.data)

    if category_form.is_valid():
        Category.objects.filter(id=request.data['id']).update(**category_form.cleaned_data)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def update_sub_category(request):
    request.data["category"] = Category.objects.get(id=request.data['category'])

    sub_category_form = SubCategoryForm(request.data)

    if sub_category_form.is_valid():
        SubCategory.objects.filter(id=request.data['id']).update(**sub_category_form.cleaned_data)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def get_category(request):
    existed_category = Category.objects.filter(id=request.data['id'])

    if existed_category:
        result = model_to_dict(existed_category.first())
        return JsonResponse({"result": result, "status": "success"})
    return JsonResponse({"status": "failure"})


@api_view(("post",))
def get_sub_category(request):
    existed_category = SubCategory.objects.filter(id=request.data['id'])

    if existed_category:
        result = model_to_dict(existed_category.first())
        return JsonResponse({"result": result, "status": "success"})
    return JsonResponse({"status": "failure"})
