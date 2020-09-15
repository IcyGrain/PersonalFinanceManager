from django.contrib import admin
from .models import *
# Register your models here.


class BudgetAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'date', 'category', 'budget_type', 'start_date', 'end_date']


admin.site.register(Budget, BudgetAdmin)
