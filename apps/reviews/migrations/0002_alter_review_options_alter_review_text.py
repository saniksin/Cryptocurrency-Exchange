# Generated by Django 4.2.1 on 2023-06-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.CharField(max_length=100, verbose_name='Комментарий'),
        ),
    ]