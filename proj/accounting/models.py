
from audioop import reverse
from django.db import models
# from utility.models import User, UserProfile
from erp.models import User
from sales.models import *
from datetime import datetime
# from django.contrib.auth.models import User

# Create your models here.


# implement billing and invoice
class Billing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    # price = models.ForeignKey(
    #     Product, on_delete=models.CASCADE, null=True, related_name='amount_sold')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    transaction_date = models.DateField(default=datetime.now, blank=False)

    def __str__(self):
        return f'{self.product} sold!'
