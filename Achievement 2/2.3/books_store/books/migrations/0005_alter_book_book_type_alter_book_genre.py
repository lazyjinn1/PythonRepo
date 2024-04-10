# Generated by Django 4.2.11 on 2024-04-10 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_book_type_alter_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_type',
            field=models.CharField(choices=[('audiobook', 'Audio Book'), ('ebook', 'E-book'), ('hardcover', 'Hard cover')], default='hc', max_length=12),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('romantic', 'Romantic'), ('comedy', 'Comedy'), ('horror', 'Horror'), ('classic', 'Classic'), ('educational', 'Educational'), ('fantasy', 'Fantasy')], default='cl', max_length=12),
        ),
    ]
