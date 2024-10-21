from django.contrib import admin
from .models import Transaction, Discount, Sale, SpecialDiscount, StockAlert, SalesAnalytics, CustomerAnalytics, Payment, Receipt, Return, Refund
# Register your models here.

admin.site.register(Transaction)
admin.site.register(Discount)
admin.site.register(Sale)
admin.site.register(SpecialDiscount)
admin.site.register(StockAlert)
admin.site.register(SalesAnalytics)
admin.site.register(CustomerAnalytics)
admin.site.register(Payment)
admin.site.register(Receipt)
admin.site.register(Return)
admin.site.register(Refund)