from django.db import models

# Create your models here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class SubCategory(models.Model):
    category = models.ForeignKey(to="Category", to_field="id", on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=100)

    def __str__(self):
        return "{}:{}".format(self.category, self.sub_category)
