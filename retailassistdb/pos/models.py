from django.utils import timezone
from django.db import models
from django.apps import apps
from django.db.models import Sum, Count

class Transaction(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey('core.Employee', on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(max_length=50, default="Cash")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(default=timezone.now)
    points_earned = models.PositiveIntegerField(default=0)
    items = models.ManyToManyField('core.Product', through='pos.Sale', related_name='transactions')

    def __str__(self):
        return (
            f"Transaction ID: {self.id}\n"
            f"Transaction Date: {self.date}\n" 
            f"Items: {self.items}\n"
            f"Amount: {self.amount}\n " 
            f"Customer ID: {self.customer.id}\n"
            f"Points Earned: {self.points_earned}\n"
            f"Employee ID: {self.employee.id}\n"
        )
    
    def calculate_total(self):
        self.total_amount = sum(sale.subtotal for sale in self.sales.all())
        self.save()
        
    def calculate_loyalty_points(self):
        self.points_earned = int(self.total_amount / 10)  # Example: 1 point per $10 spent
        self.customer.add_loyalty_points(self.points_earned)
        self.save()

    @staticmethod
    def calculate_profit(transactions):
        total_revenue = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        total_cost = sum(transaction.product.cost_price * transaction.items.count() for transaction in transactions)
        return total_revenue - total_cost

    @staticmethod
    def get_top_selling_product(transactions):
        top_product = transactions.values('product__name').annotate(total_sold=Count('product')).order_by('-total_sold').first()
        return top_product['product__name'] if top_product else None

    @staticmethod
    def get_top_customer(transactions):
        top_customer = transactions.values('customer__name').annotate(total_spent=Sum('amount')).order_by('-total_spent').first()
        return top_customer['customer__name'] if top_customer else None
        
class Discount(models.Model):
    name = models.CharField(max_length=255)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add default value
    special_conditions = models.TextField(default="No special conditions")

    def __str__(self):
        return f"Discount {self.amount} from {self.valid_from} to {self.valid_until}"
            
    
class SpecialDiscount(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    valid_until = models.DateField(default=timezone.now)
    special_conditions = models.TextField(default="No special conditions")

    def __str__(self):
        return f"Discount {self.discount_percent}% on {self.product.name} from {self.start_date} to {self.end_date}"
    
class StockAlert(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    threshold = models.PositiveIntegerField(default=150)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Stock Alert for {self.product.name} at {self.alert_threshold} on {self.alert_date}"
    
class SalesAnalytics(models.Model):
    report_date = models.DateField(default=timezone.now)
    total_sales_value = models.DecimalField(max_digits=12, decimal_places=2)
    top_selling_product = models.ForeignKey('core.Product', on_delete=models.CASCADE, null=True)
    num_transactions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Sales Analytics for {self.report_date} - Top selling product: {self.top_selling_product}"

    @classmethod
    def generate_sales_analytics(cls, product_id, start_date, end_date):
        sales = Sale.objects.filter(product_id=product_id, transaction__transaction_date__gte=start_date, transaction__transaction_date__lte=end_date)
        total_sales_value = sum([sale.subtotal for sale in sales])
        total_quantity_sold = sum([sale.quantity for sale in sales])
        Product = apps.get_model('core', 'Product')
        top_selling_product = Product.objects.get(id=product_id)
        return cls.objects.create(report_date=end_date, total_sales_value=total_sales_value, top_selling_product=top_selling_product, num_transactions=sales.count())
    
    
class CustomerAnalytics(models.Model):
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE, null=True)
    purchases = models.ManyToManyField('core.Product', through='pos.Sale', related_name='customer_analytics')
    total_spent = models.DecimalField(max_digits=12, decimal_places=2)
    report_date = models.DateField(default=timezone.now)
    total_loyalty_points_earned = models.PositiveIntegerField(default=0)
    total_loyalty_points_redeemed = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Customer Analytics for {self.customer.name} on {self.report_date}, Total spent: {self.total_spent}, Total loyalty points earned: {self.total_loyalty_points_earned}, Total loyalty points redeemed: {self.total_loyalty_points_redeemed}"
    
    @classmethod
    def generate_customer_analytics(cls, customer_id):
        Customer = apps.get_model('core', 'Customer')
        customer = Customer.objects.get(id=customer_id)
        transactions = Transaction.objects.filter(customer=customer)
        total_spent = sum([transaction.total_amount for transaction in transactions])
        total_loyalty_points_earned = sum([transaction.total_amount // 10 for transaction in transactions])
        return cls.objects.create(customer=customer, total_spent=total_spent, total_loyalty_points_earned=total_loyalty_points_earned)
    
class Sale(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    customer_analytics = models.ForeignKey(CustomerAnalytics, on_delete=models.CASCADE, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='sales')
    employee = models.ForeignKey('core.Employee', on_delete=models.CASCADE, null=True, default=None)  # Add default value
    date = models.DateTimeField(default=timezone.now)  # Add default value
    quantity = models.PositiveIntegerField(default=0)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add default value
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add default value
    payment_method = models.CharField(max_length=50, default="Cash")  # Add default value
    
    def __str__(self):
        return f"Sale {self.quantity} of {self.product.name} by {self.employee.name}"

    def save(self, *args, **kwargs):
        if self.subtotal is None:
            self.subtotal = self.product.price * self.quantity
        self.calculate_final_price()
        self.product.update_stock(-self.quantity)  # Deduct sold quantity from stock
        super(Sale, self).save(*args, **kwargs)

    def calculate_final_price(self):
        if self.discount:
            discount_amount = self.subtotal * (self.discount.percentage / 100)
            self.final_price = self.subtotal - discount_amount
        else:
            self.final_price = self.subtotal

class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default=None, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('M-Pesa', 'M-Pesa')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment of {self.amount} made on {self.payment_date} for transaction {self.transaction.id}"

class Receipt(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default=None, null=True)
    email = models.BooleanField(default=False)

    def __str__(self):
        return f"Receipt {self.receipt_number} for transaction {self.transaction.id} issued on {self.issued_date}"

class Return(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default=None, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, default=None, null=True)
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE, default=None, null=True)
    quantity = models.PositiveIntegerField(default=0)
    reason = models.TextField(default="No reason provided")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Return of {self.quantity} {self.product.name} from transaction {self.transaction.id}"

    def process_return(self):
        # Return stock and handle refund logic
        self.product.update_stock(self.quantity)
        
        # Adjust transaction total
        refund_amount = self.product.price * self.quantity
        self.transaction.total_amount -= refund_amount
        self.transaction.save()

        # Handle refund logic (e.g., create a refund record or update payment method)
        # This is a placeholder for actual refund processing logic
        # Example: create a refund record
        Refund.objects.create(
            transaction=self.transaction,
            amount=refund_amount,
            refund_date=timezone.now()
        )

class Refund(models.Model):
    return_sale = models.ForeignKey(Return, on_delete=models.CASCADE, default=None, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, default=None, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    refund_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Refund of {self.amount} for transaction {self.transaction.id}"