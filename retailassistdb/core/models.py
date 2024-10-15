from django.db import models
from django.utils import timezone
from django.apps import apps

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, null=True)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)
    barcode = models.CharField(max_length=13, default="0000000000000")

    def __str__(self):
        return (
            f"Product name: {self.name}\n"
            f"Sku: {self.sku}\n"
            f"Price: {self.price}\n"
            f"Stock: {self.stock}\n"
            f"Supplier: {self.supplier}\n"
            f"Low Stock Threshold: {self.low_stock_threshold}\n"
            f"Last Updated: {self.last_updated}\n"
            f"Barcode: {self.barcode}"
        )

    def update_stock(self, quantity):
        if self.stock + quantity < 0:
            raise ValueError("Insufficient stock to complete the sale.")
        self.stock += quantity
        self.save()
        
    def is_low_stock(self):
        return self.stock < self.low_stock_threshold

from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, default="0000000000")
    loyalty_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Email: {self.email}\n"
            f"Phone: {self.phone}\n"
            f"Loyalty Points: {self.loyalty_points}"
        )
    
    def add_loyalty_points(self, points):
        self.loyalty_points += points
        self.save()

class Employee(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, default="0000000000")
    email = models.EmailField(unique=True, null=True, blank=True)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    shift_schedule = models.CharField(max_length=255)

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Phone: {self.phone}\n"
            f"Email: {self.email}\n"
            f"Position: {self.position}\n"
            f"Hire Date: {self.hire_date}\n"
            f"Shift Schedule: {self.shift_schedule}"
        )

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default="123 Supplier St, Supplier City, Supplier Country")
    phone = models.CharField(max_length=15, default="0000000000")
    email = models.EmailField()
    delivery_times = models.CharField(max_length=255)

    def __str__(self):
        return (
            f"{self.name}\n"
            f"Contact Person: {self.contact_person}\n"
            f"Phone: {self.phone}\n"
            f"Email: {self.email}\n"
            f"Delivery Times: {self.delivery_times}"
        )

class RevenueReport(models.Model):
    report_date = models.DateField(default=timezone.now)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    total_profit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Revenue Report for {self.report_date} : Total Revenue: {self.total_revenue}, Total Profit: {self.total_profit}"

    @classmethod
    def generate_report(cls, start_date, end_date):
        Transaction = apps.get_model('pos', 'Transaction')
        transactions = Transaction.objects.filter(transaction_date__gte=start_date, transaction_date__lte=end_date)
        total_revenue = sum([transaction.total_amount for transaction in transactions])
        total_profit = cls.calculate_profit(transactions)
        return cls.objects.create(total_revenue=total_revenue, total_profit=total_profit)

    @staticmethod
    def calculate_profit(transactions):
        return sum([transaction.total_amount * 0.2 for transaction in transactions]) * 0.2

class ExpenseReport(models.Model):
    report_date = models.DateField(default=timezone.now)
    description = models.TextField()
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Expense Report for {self.report_date} : {self.description} - Total Expenses: {self.total_expenses}"

    @classmethod
    def generate_report(cls, start_date, end_date):
        total_expenses = sum([1000, 2000, 3000])
        return cls.objects.create(total_expenses=total_expenses)

class DataAnalytics(models.Model):
    report_date = models.DateField(default=timezone.now)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    total_profit = models.DecimalField(max_digits=12, decimal_places=2)
    top_selling_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    top_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return (
            f"Data Analytics for {self.report_date}\n"
            f"Total Sales: {self.total_sales}\n"
            f"Total Expenses: {self.total_expenses}\n"
            f"Total Profit: {self.total_profit}\n"
            f"Top Selling Product: {self.top_selling_product}\n"
            f"Top Customer: {self.top_customer}"
        )

    @classmethod
    def generate_data_analytics(cls, start_date, end_date):
        Transaction = apps.get_model('pos', 'Transaction')
        transactions = Transaction.objects.filter(transaction_date__gte=start_date, transaction_date__lte=end_date)
        total_sales = sum([transaction.total_amount for transaction in transactions])
        total_expenses = sum([1000, 2000, 3000])
        total_profit = cls.calculate_profit(transactions)
        top_selling_product = cls.get_top_selling_product(transactions)
        top_customer = cls.get_top_customer(transactions)
        
class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return (
            f"Shift for {self.employee.name}\n"
            f"Start Time: {self.start_time}\n"
            f"End Time: {self.end_time}\n"
            f"Total Sales: {self.total_sales}\n"
            f"Total Cash: {self.total_cash}"
        )

    def close_shift(self):
        self.end_time = timezone.now()
        # Logic to calculate totals and close shift
        Sale = apps.get_model('pos', 'Sale')
        Payment = apps.get_model('pos', 'Payment')
        sales = Sale.objects.filter(employee=self.employee, date__range=(self.start_time, self.end_time))
        self.total_sales = sum(sale.final_price for sale in sales)
        self.total_cash = sum(payment.amount for payment in Payment.objects.filter(transaction__sales__in=sales, method='Cash'))
        self.save()