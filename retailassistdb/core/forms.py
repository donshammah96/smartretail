from django import forms
from .models import Product, Supplier, Customer, Employee, RevenueReport, ExpenseReport, DataAnalytics, Shift, Category, RevenueReportManager


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class SaleForm(forms.Form):
    class Meta:
        model = Product
        fields = '__all__'

class AddSaleForm(forms.Form):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerForm(forms.Form):
    class Meta:
        model = Customer
        fields = '__all__'

class AddCustomerForm(forms.Form):
    class Meta:
        model = Customer
        fields = '__all__'

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class UpdateStockForm(forms.Form):
    class Meta:
        model = Product
        fields = '__all__'

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseReport
        fields = '__all__'

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseReport
        fields = '__all__'

class RevenueForm(forms.ModelForm):
    class Meta:
        model = RevenueReport
        fields = '__all__'

class AddRevenueForm(forms.ModelForm):
    class Meta:
        model = RevenueReport
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class EditSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'

class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class RevenueReportForm(forms.ModelForm):
    class Meta:
        model = RevenueReport
        fields = '__all__'

class EditRevenueReportForm(forms.ModelForm):
    class Meta:
        model = RevenueReport
        fields = '__all__'

class ExpenseReportForm(forms.ModelForm):
    class Meta:
        model = ExpenseReport
        fields = '__all__'

class EditExpenseReportForm(forms.ModelForm):
    class Meta:
        model = ExpenseReport
        fields = '__all__'

class DataAnalyticsForm(forms.ModelForm):
    class Meta:
        model = DataAnalytics
        fields = '__all__'

class EditDataAnalyticsForm(forms.ModelForm):
    class Meta:
        model = DataAnalytics
        fields = '__all__'

class AddDataAnalyticsForm(forms.ModelForm):
    class Meta:
        model = DataAnalytics
        fields = '__all__'

class EditDataAnalyticsForm(forms.ModelForm):
    class Meta:
        model = DataAnalytics
        fields = '__all__'

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class RevenueReportForm(forms.ModelForm):
    class Meta:
        model = RevenueReport
        fields = '__all__'