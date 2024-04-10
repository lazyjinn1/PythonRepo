from django.db import models

genre_choices = {
    ('classic', 'Classic'),
    ('romantic', 'Romantic'),
    ('comedy', 'Comedy'),
    ('fantasy', 'Fantasy'),
    ('horror', 'Horror'),
    ('educational', 'Educational'),
}

book_type_choices = {
    ('hardcover', 'Hard cover'),
    ('ebook', 'E-book'),
    ('audiobook', 'Audio Book')
}

class Book(models.Model):
    name = models.CharField(max_length = 120)
    author_name = models.CharField(max_length = 120)
    genre = models.CharField(max_length = 12, choices=genre_choices, default = 'cl')
    book_type = models.CharField(max_length = 12, choices=book_type_choices, default = 'hc')
    price = models.FloatField(help_text='in US dollars $')

    def __str__(self):
        return str(self.name)