# Generated by Django 4.2.1 on 2023-06-25 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=150, verbose_name='Комментарий'),
        ),
    ]
