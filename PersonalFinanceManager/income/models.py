from django.db import models
import django.utils.timezone as timezone
from account.models import *
# Create your models here.


class Income(models.Model):
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField(default=timezone.now)
    account = models.ForeignKey(Account, to_field="id", on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    note = models.TextField()

