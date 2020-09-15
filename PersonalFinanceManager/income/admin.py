from django.contrib import admin
from .models import *

# Register your models here.


class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'date', 'account', 'source', 'note']


admin.site.register(Income, IncomeAdmin)

