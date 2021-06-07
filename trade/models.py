from decimal import Decimal
from django.db import models
from django.conf import settings 

# Create your models here.

 
class UserProfile(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def reset_account(self):
        self.balance = Decimal("5000.00")
        self.save()

    def get_share_count(self, stock_name):
        transactions = self.transactions.filter(stock_name=stock_name)
        
        share_count = 0

        for transaction in transactions:
            if transaction.transaction_type == "BUY":
                share_count += transaction.num_of_shares
            else:
                share_count -= transaction.num_of_shares

        return share_count


    #str method create
    def __str__(self):
        return "{} {}".format(self.user,self.balance)



class Transactions(models.Model):

    STOCK_NAMES = [
        ("TSLA", "TESLA"),
        ("BMW.DE", "Bayerische Motoren Werke Aktiengesellschaft"),
    ]
    TRANSACTION_TYPES = [
        ("BUY", "Buy"),
        ("SELL", "Sell"),
    ]

    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, related_name="transactions")
    date_time = models.DateTimeField(auto_now_add=True)
    num_of_shares = models.PositiveIntegerField()
    stock_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of each unit share") 
    stock_name = models.CharField(max_length=7, choices=STOCK_NAMES)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    cash_impact = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    

    def save(self, *args, **kwargs):
        self.cash_impact = self.num_of_shares * self.stock_price #{{ stock_data.current }}

        super().save(*args, **kwargs)


