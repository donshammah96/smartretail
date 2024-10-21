from django.contrib import admin
from .models import Product, Customer, Employee, Supplier, RevenueReport, ExpenseReport, DataAnalytics, Shift

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(RevenueReport)
admin.site.register(ExpenseReport)
admin.site.register(DataAnalytics)
admin.site.register(Shift)