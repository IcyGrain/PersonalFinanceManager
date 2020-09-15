from django.contrib import admin
from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_id', 'sub_category']


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)

