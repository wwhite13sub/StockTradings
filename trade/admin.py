from django.contrib import admin
from trade import models as trade_models
# Register your models here.
admin.site.register(trade_models.UserProfile)
admin.site.register(trade_models.Transactions)
