import django.utils.timezone as timezone
from django.db import models
from category.models import *
# Create your models here.


class Budget(models.Model):
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(SubCategory, to_field="id", on_delete=models.CASCADE)
    budget_type = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
