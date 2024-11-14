"""
This module contains the models for the core app.
"""

from django.db import models
from django.utils import timezone
from django.apps import apps
from pos.models import Sale, Transaction, Inventory
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum


# Function to mask phone numbers (replace with your preferred masking logic)
def mask_phone_number(phone_number):
    """
    Mask the phone number for privacy.
    """
    if len(phone_number) > 10:
        return phone_number[:3] + "***" + phone_number[-4:]
    return phone_number


class Supplier(models.Model):
    """
    Model representing a supplier.
    """

    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    address = models.CharField(
        max_length=255, default="123 Supplier St, Supplier City, Supplier Country"
    )
    phone = models.CharField(max_length=15, default="")
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


class Category(models.Model):
    """
    Model representing a product category.
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Model representing a product.
    """

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name="products"
    )
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    supplier = models.ForeignKey(
        "Supplier", on_delete=models.SET_NULL, null=True, related_name="products"
    )
    low_stock_threshold = models.PositiveIntegerField(default=10)
    last_updated = models.DateTimeField(auto_now=True)
    barcode = models.CharField(max_length=13, unique=True)
    expiration_date = models.DateField(null=True, blank=True)
    restock_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.sku}"

    @property
    def stock(self):
        """
        Return the current stock level.
        """
        try:
            return self.inventory.current_stock
        except Inventory.DoesNotExist:
            return 0

    def update_stock(self, quantity, reason=""):
        """
        Updates the stock level through the related Inventory object.
        """
        try:
            return self.inventory.update_stock(adjustment=quantity, reason=reason)
        except Inventory.DoesNotExist:
            Inventory.objects.create(
                product=self, current_stock=quantity, initial_stock=quantity
            )
            return quantity

    def is_low_stock(self):
        """
        Check if the stock level is below the low stock threshold.
        """
        return self.stock < self.low_stock_threshold

    def save(self, *args, **kwargs):
        """
        Save the product and ensure the Inventory object is created or updated.
        """
        super().save(*args, **kwargs)
        try:
            inventory = self.inventory
            if inventory.reorder_level != self.low_stock_threshold:
                inventory.reorder_level = self.low_stock_threshold
                inventory.save()
        except Inventory.DoesNotExist:
            Inventory.objects.create(
                product=self, reorder_level=self.low_stock_threshold
            )


class Customer(models.Model):
    """
    Model representing a customer.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

    def add_loyalty_points(self, points):
        """
        Add loyalty points to the customer.
        """
        self.loyalty_points += points
        self.save()


class Employee(models.Model):
    """
    Model representing an employee.
    """

    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    position = models.CharField(max_length=100)
    hire_date = models.DateField(default=timezone.now)
    shift_schedule = models.ForeignKey(
        "Shift", on_delete=models.CASCADE, null=True, related_name="scheduled_employees"
    )
    total_sales = models.OneToOneField(
        Sale, on_delete=models.CASCADE, null=True, related_name="employee"
    )
    average_transaction_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    performance_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    assigned_shifts = models.ManyToManyField(
        "Shift", related_name="assigned_employees", blank=True
    )

    @property
    def total_sales(self):
        """
        Return the total sales made by the employee.
        """
        total = self.sales.aggregate(total_sales=Sum("final_price"))["total_sales"]
        return total if total is not None else 0

    def __str__(self):
        return (
            f"Name: {self.name}\n"
            f"Phone: {self.phone_number}\n"
            f"Email: {self.email}\n"
            f"Position: {self.position}\n"
            f"Hire Date: {self.hire_date}\n"
            f"Shift Schedule: {self.shift_schedule}"
        )


class ExpenseReport(models.Model):
    """
    Model representing an expense report.
    """

    report_date = models.DateField(default=timezone.now)
    description = models.TextField(null=True, blank=True)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Expense Report for {self.report_date} : {self.description} - Total Expenses: {self.total_expenses:.2f}"

    @classmethod
    def generate_report(cls, start_date, end_date):
        """
        Generate an expense report for the given date range.
        """
        total_expenses = sum([1000, 2000, 3000])
        return cls.objects.create(total_expenses=total_expenses)


class DataAnalytics(models.Model):
    """
    Model representing data analytics.
    """

    report_date = models.DateField(default=timezone.now)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2)
    total_profit = models.DecimalField(max_digits=12, decimal_places=2)
    top_selling_product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        null=True,
        related_name="top_selling_product",
    )
    top_customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, null=True, related_name="top_customer"
    )
    metrics = models.TextField(null=True, blank=True)
    insights = models.TextField(null=True, blank=True)

    def __str__(self):
        return (
            f"Data Analytics for {self.report_date}\n"
            f"Total Sales: {self.total_sales:.2f}\n"
            f"Total Expenses: {self.total_expenses}\n"
            f"Total Profit: {self.total_profit:.2f}\n"
            f"Top Selling Product: {self.top_selling_product}\n"
            f"Top Customer: {self.top_customer}\n"
            f"Metrics: {self.metrics}\n"
            f"Insights: {self.insights}"
        )

    @classmethod
    def generate_data_analytics(cls, start_date, end_date):
        """
        Generate data analytics for the given date range.
        """
        Transaction = apps.get_model("pos", "Transaction")
        transactions = Transaction.objects.filter(
            transaction_date__gte=start_date, transaction_date__lte=end_date
        )
        total_sales = sum(transaction.total_amount for transaction in transactions)
        total_expenses = sum([1000, 2000, 3000])
        total_profit = cls.calculate_profit(transactions)
        top_selling_product = cls.get_top_selling_product(transactions)
        top_customer = cls.get_top_customer(transactions)
        metrics = "Some metrics data"
        insights = "Some insights data"
        return cls.objects.create(
            report_date=timezone.now(),
            total_sales=total_sales,
            total_expenses=total_expenses,
            total_profit=total_profit,
            top_selling_product=top_selling_product,
            top_customer=top_customer,
            metrics=metrics,
            insights=insights,
        )


class Shift(models.Model):
    """
    Model representing a work shift.
    """

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="shifts"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return (
            f"Shift for {self.employee.name}\n"
            f"Start Time: {self.start_time}\n"
            f"End Time: {self.end_time}\n"
            f"Total Sales: {self.total_sales:.2f}\n"
            f"Total Cash: {self.total_cash:.2f}"
        )

    def close_shift(self):
        """
        Close the shift and calculate totals.
        """
        self.end_time = timezone.now()
        Sale = apps.get_model("pos", "Sale")
        Payment = apps.get_model("pos", "Payment")
        sales = Sale.objects.filter(
            employee=self.employee, date__range=(self.start_time, self.end_time)
        )
        self.total_sales = sum(sale.final_price for sale in sales)
        self.total_cash = sum(
            payment.amount
            for payment in Payment.objects.filter(
                transaction__sales__in=sales, method="Cash"
            )
        )
        self.save()


class RevenueReportManager(models.Manager):
    """
    Manager for generating revenue reports.
    """

    def generate_report(self, start_date, end_date):
        """
        Generate a revenue report for the given date range.
        """
        transactions = Transaction.objects.filter(
            transaction_date__gte=start_date, transaction_date__lte=end_date
        )
        total_revenue = sum(transaction.amount for transaction in transactions)
        total_profit = self.calculate_profit(transactions)
        return self.create(total_revenue=total_revenue, total_profit=total_profit)

    def calculate_profit(self, transactions):
        """
        Calculate profit from transactions.
        """
        return sum(transaction.amount * 0.2 for transaction in transactions) * 0.2


class RevenueReport(models.Model):
    """
    Model representing a revenue report.
    """

    report_date = models.DateTimeField(default=timezone.now)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    total_profit = models.DecimalField(max_digits=12, decimal_places=2)
    details = models.JSONField(null=True, blank=True)

    objects = RevenueReportManager()

    def __str__(self):
        return f"Revenue Report - {self.report_date.date()}"
