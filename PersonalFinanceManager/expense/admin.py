from django.contrib import admin
from .models import *
# Register your models here.


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'date', 'category', 'account', 'payee', 'note']


admin.site.register(Expense, ExpenseAdmin)
