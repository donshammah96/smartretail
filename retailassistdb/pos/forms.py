from django import forms
from .models import Transaction, Discount, Sale, SpecialDiscount, StockAlert, SalesAnalytics, CustomerAnalytics, Payment, Receipt, Return, Refund, Inventory, InventoryAdjustment

# Define forms for the models
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

class SpecialDiscountForm(forms.ModelForm):
    class Meta:
        model = SpecialDiscount
        fields = '__all__'

class StockAlertForm(forms.ModelForm):
    class Meta:
        model = StockAlert
        fields = '__all__'

class SalesAnalyticsForm(forms.ModelForm):
    class Meta:
        model = SalesAnalytics
        fields = '__all__'

class CustomerAnalyticsForm(forms.ModelForm):
    class Meta:
        model = CustomerAnalytics
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = '__all__'

class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = '__all__'

class EditSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

class CreateTransactionForm(forms.Form):
    class Meta:
        model = Transaction
        fields = '__all__'

class EditTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'
class InventoryAdjustmentForm(forms.ModelForm):
    class Meta:
        model = InventoryAdjustment
        fields = '__all__'