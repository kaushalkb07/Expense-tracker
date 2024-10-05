from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Expense(models.Model):
    CATEGORY_CHOICES = (
        ('CLOTHING', 'Clothing'),
        ('FOOD', 'Food'),
        ('TRANSPORT', 'Transport'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('MISCELLANEOUS', 'Miscellaneous'),
        ('OTHER', 'Other'),
    )
    sno = models.AutoField(primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    slug = models.CharField(max_length = 255)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return 'Expense of ' + self.title + ' on ' + self.category