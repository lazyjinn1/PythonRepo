# Generated by Django 4.2.11 on 2024-04-17 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='pic',
            field=models.ImageField(default='no-picture.jpg', upload_to='recipes'),
        ),
    ]
