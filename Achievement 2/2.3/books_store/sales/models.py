from django.db import models

book_choices = {
    
}

class Sale(models.Model):
    name = models.CharField(max_length=120)
    book = models.CharField(max_length = 40, choices=book_choices, default = 'hc')
    date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return str(self.name)