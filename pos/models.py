from django.utils import timezone
from django.db import models
from django.apps import apps
from django.db.models import Sum, Count
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Inventory(models.Model):
    product = models.OneToOneField('core.Product', on_delete=models.CASCADE, related_name='inventory')
    initial_stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    current_stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    reorder_level = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Inventory for {self.product.name} - Current stock: {self.current_stock}"

    def update_stock(self, adjustment, reason=""):
        """
        Update the stock level based on an adjustment. Positive for adding stock, negative for reducing.
        """
        if self.current_stock + adjustment < 0:
            raise ValueError("Insufficient stock to complete the adjustment.") 

        self.current_stock += adjustment
        self.save()

        # Record the adjustment history
        InventoryAdjustment.objects.create(
            inventory=self,
            adjustment=adjustment,
            reason=reason
        )
        return self.current_stock

    def is_reorder_needed(self):
        return self.current_stock <= self.reorder_level


class InventoryAdjustment(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='adjustments')
    adjustment = models.IntegerField()
    reason = models.TextField()
    adjustment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Adjustment for {self.inventory.product.name}: {self.adjustment} units on {self.adjustment_date}"


@receiver(post_save, sender='core.Product')
def create_inventory(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(product=instance)


class Purchase(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE, related_name='purchases')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cost_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateTimeField(default=timezone.now)
    supplier = models.CharField(max_length=255, null=True, blank=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='purchases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchase of {self.quantity} units of {self.product.name}"

    def save(self, *args, **kwargs):
        # Calculate total cost
        self.total_cost = self.cost_price_per_unit * self.quantity
        super().save(*args, **kwargs)
        # Update the inventory stock level
        self.inventory.update_stock(self.quantity, reason=f"Purchase: {self.quantity} units added")

class Transaction(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE, related_name='transactions')
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    employee = models.ForeignKey('core.Employee', on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('M-Pesa', 'M-Pesa')], default='Cash')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    date = models.DateTimeField(default=timezone.now)
    points_earned = models.PositiveIntegerField(default=0)
    items = models.ManyToManyField('core.Product', through='pos.Sale', related_name='transaction_items')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Transaction {self.id} on {self.date}"

    def calculate_total(self):
        self.amount = self.sales.aggregate(total=Sum('subtotal'))['total'] or 0.00
        self.save()

    def calculate_loyalty_points(self):
        self.points_earned = int(self.amount / 10)
        if self.customer:
            self.customer.add_loyalty_points(self.points_earned)
        self.save()

    @staticmethod
    def calculate_profit(transactions):
        total_revenue = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        total_cost = transactions.annotate(
            cost=models.F('product__cost_price') * models.F('items__count')
        ).aggregate(total_cost=Sum('cost'))['total_cost'] or 0
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
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    special_conditions = models.TextField(default="No special conditions")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Discount {self.amount} from {self.valid_from} to {self.valid_until}"


class SpecialDiscount(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE, related_name='special_discounts')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    valid_until = models.DateField(default=timezone.now)
    special_conditions = models.TextField(default="No special conditions")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Discount {self.discount_percent}% on {self.product.name} until {self.valid_until}"


class StockAlert(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE, related_name='stock_alerts')
    threshold = models.PositiveIntegerField(default=150, validators=[MinValueValidator(1)])
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Stock Alert for {self.product.name} at threshold {self.threshold} on {self.date}"


class SalesAnalytics(models.Model):
    report_date = models.DateField(default=timezone.now)
    total_sales_value = models.DecimalField(max_digits=12, decimal_places=2)
    top_selling_product = models.ForeignKey('core.Product', on_delete=models.CASCADE, null=True, related_name='sales_analytics')
    num_transactions = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sales Analytics for {self.report_date} - Top selling product: {self.top_selling_product}"

    @classmethod
    def generate_sales_analytics(cls, product_id, start_date, end_date):
        sales = Sale.objects.filter(product_id=product_id, transaction__date__range=(start_date, end_date))
        total_sales_value = sales.aggregate(total_value=Sum('subtotal'))['total_value'] or 0
        top_selling_product = apps.get_model('core', 'Product').objects.get(id=product_id)
        return cls.objects.create(report_date=end_date, total_sales_value=total_sales_value, top_selling_product=top_selling_product, num_transactions=sales.count())


class CustomerAnalytics(models.Model):
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, related_name='analytics', blank=True, null=True)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2)
    report_date = models.DateField(default=timezone.now)
    total_loyalty_points_earned = models.PositiveIntegerField(default=0)
    total_loyalty_points_redeemed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return f"Customer Analytics for {self.customer.name} on {self.report_date}"

    @classmethod
    def generate_customer_analytics(cls, customer_id):
        customer = apps.get_model('core', 'Customer').objects.get(id=customer_id)
        transactions = Transaction.objects.filter(customer=customer)
        total_spent = transactions.aggregate(total=Sum('amount'))['total'] or 0
        total_loyalty_points_earned = transactions.aggregate(points=Sum('points_earned'))['points'] or 0
        return cls.objects.create(customer=customer, total_spent=total_spent, total_loyalty_points_earned=total_loyalty_points_earned)


class Sale(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE, related_name='sales')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='sales')
    employee = models.ForeignKey('core.Employee', on_delete=models.CASCADE, null=True, blank=True, related_name='sales')
    date = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1)])
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True, blank=True, related_name='sales')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    final_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=50, default="Cash")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale of {self.quantity} {self.product.name}"

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        self.calculate_final_price()
        self.product.update_stock(-self.quantity)
        super().save(*args, **kwargs)

    def calculate_final_price(self):
        if self.discount:
            discount_amount = self.subtotal * (self.discount.amount / 100)
            self.final_price = self.subtotal - discount_amount
        else:
            self.final_price = self.subtotal


class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('M-Pesa', 'M-Pesa')])
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    payment_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment of {self.amount} for transaction {self.transaction.id}"


class Return(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='returns')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='returns')
    return_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    reason = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Return for sale {self.sale.id} on {self.date}"

    def process_return(self):
        if self.return_quantity <= self.sale.quantity:
            self.sale.product.update_stock(self.return_quantity)
            self.status = 'Approved'
            self.save()
        else:
            self.status = 'Rejected'
            self.save()


class Refund(models.Model):
    return_sale = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='refunds', blank=True, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Refund for return {self.return_sale.id} of transaction {self.transaction.id}"


class Receipt(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='receipts')
    email_sent = models.BooleanField(default=False)
    receipt_number = models.CharField(max_length=100, unique=True)
    generated_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Receipt for transaction {self.transaction.id}"

    def send_via_email(self):
        # Implement email sending logic here
        self.email_sent = True
        self.save()
