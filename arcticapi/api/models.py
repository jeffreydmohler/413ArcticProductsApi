from django.db import models
from api.fields import JSONField

# Create your models here.
class Category(models.Model):
    title = models.TextField(unique=True)

class Product(models.Model):
    filename = models.TextField()
    name = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class Sale(models.Model):
    name = models.TextField()
    address1 = models.TextField()
    address2 = models.TextField(null=True, blank=True)
    city = models.TextField()
    state = models.TextField()
    zipcode = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    items = JSONField(default=dict) # import our JSONField at top of file
    payment_intent = JSONField(default=dict) # stripe thing - for next week