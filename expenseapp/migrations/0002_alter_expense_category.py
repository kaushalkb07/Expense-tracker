# Generated by Django 5.1.1 on 2024-10-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenseapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('CLOTHING', 'Clothing'), ('FOOD', 'Food'), ('TRANSPORT', 'Transport'), ('ENTERTAINMENT', 'Entertainment'), ('MISCELLANEOUS', 'Miscellaneous'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
    ]
