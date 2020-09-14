from django.contrib import admin
from .models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'sub_category']


class AccountAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'account_type', 'currency', "balance"]


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'amount', 'date', 'category', 'account', 'payee', 'note']


class IncomeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'amount', 'date', 'account', 'source', 'note']


class BudgetAdmin(admin.ModelAdmin):
    list_display = ['pk', 'amount', 'date', 'category', 'budget_type', 'start_date', 'end_date']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Budget, BudgetAdmin)
