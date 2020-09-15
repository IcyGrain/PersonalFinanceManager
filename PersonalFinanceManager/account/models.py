from django.db import models


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.name
