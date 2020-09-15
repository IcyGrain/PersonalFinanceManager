import django.utils.timezone as timezone
from django.db import models
from category.models import *
from account.models import *
# Create your models here.


class Expense(models.Model):
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(SubCategory, to_field="id", on_delete=models.CASCADE)
    account = models.ForeignKey(Account, to_field="id", on_delete=models.CASCADE)
    payee = models.CharField(max_length=100)
    note = models.TextField()
