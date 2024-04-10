from django.db import models

class SalesPerson(models.Model):
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=25)
    bio = models.TextField()

    class Meta:
        verbose_name_plural = "Sales Persons"

    def __str__(self):
        return str(self.name)