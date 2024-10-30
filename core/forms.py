"""
This module contains form definitions for the core app.
"""

from django import forms
from .models import (
    Product,
    Supplier,
    Customer,
    Employee,
    RevenueReport,
    ExpenseReport,
    DataAnalytics,
    Shift,
    Category,
)


class EmployeeForm(forms.ModelForm):
    """
    Form for creating and updating Employee instances.
    """

    class Meta:
        model = Employee
        fields = "__all__"


class AddEmployeeForm(forms.ModelForm):
    """
    Form for adding new Employee instances.
    """

    class Meta:
        model = Employee
        fields = "__all__"


class SupplierForm(forms.ModelForm):
    """
    Form for creating and updating Supplier instances.
    """

    class Meta:
        model = Supplier
        fields = "__all__"


class AddSupplierForm(forms.ModelForm):
    """
    Form for adding new Supplier instances.
    """

    class Meta:
        model = Supplier
        fields = "__all__"


class SaleForm(forms.ModelForm):
    """
    Form for creating and updating Sale instances.
    """

    class Meta:
        model = Product
        fields = "__all__"


class AddSaleForm(forms.ModelForm):
    """
    Form for adding new Sale instances.
    """

    class Meta:
        model = Product
        fields = "__all__"


class CustomerForm(forms.ModelForm):
    """
    Form for creating and updating Customer instances.
    """

    class Meta:
        model = Customer
        fields = "__all__"


class AddCustomerForm(forms.ModelForm):
    """
    Form for adding new Customer instances.
    """

    class Meta:
        model = Customer
        fields = "__all__"


class AddProductForm(forms.ModelForm):
    """
    Form for adding new Product instances.
    """

    class Meta:
        model = Product
        fields = "__all__"


class UpdateStockForm(forms.ModelForm):
    """
    Form for updating stock of Product instances.
    """

    class Meta:
        model = Product
        fields = "__all__"


class ExpenseForm(forms.ModelForm):
    """
    Form for creating and updating ExpenseReport instances.
    """

    class Meta:
        model = ExpenseReport
        fields = "__all__"


class AddExpenseForm(forms.ModelForm):
    """
    Form for adding new ExpenseReport instances.
    """

    class Meta:
        model = ExpenseReport
        fields = "__all__"


class RevenueForm(forms.ModelForm):
    """
    Form for creating and updating RevenueReport instances.
    """

    class Meta:
        model = RevenueReport
        fields = "__all__"


class AddRevenueForm(forms.ModelForm):
    """
    Form for adding new RevenueReport instances.
    """

    class Meta:
        model = RevenueReport
        fields = "__all__"


class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances.
    """

    class Meta:
        model = Product
        fields = "__all__"


class EditProductForm(forms.ModelForm):
    """
    Form for editing existing Product instances.
    """

    class Meta:
        model = Product
        fields = "__all__"


class EditSupplierForm(forms.ModelForm):
    """
    Form for editing existing Supplier instances.
    """

    class Meta:
        model = Supplier
        fields = "__all__"


class EditCustomerForm(forms.ModelForm):
    """
    Form for editing existing Customer instances.
    """

    class Meta:
        model = Customer
        fields = "__all__"


class EditEmployeeForm(forms.ModelForm):
    """
    Form for editing existing Employee instances.
    """

    class Meta:
        model = Employee
        fields = "__all__"


class RevenueReportForm(forms.ModelForm):
    """
    Form for creating and updating RevenueReport instances.
    """

    class Meta:
        model = RevenueReport
        fields = "__all__"


class EditRevenueReportForm(forms.ModelForm):
    """
    Form for editing existing RevenueReport instances.
    """

    class Meta:
        model = RevenueReport
        fields = "__all__"


class ExpenseReportForm(forms.ModelForm):
    """
    Form for creating and updating ExpenseReport instances.
    """

    class Meta:
        model = ExpenseReport
        fields = "__all__"


class EditExpenseReportForm(forms.ModelForm):
    """
    Form for editing existing ExpenseReport instances.
    """

    class Meta:
        model = ExpenseReport
        fields = "__all__"


class DataAnalyticsForm(forms.ModelForm):
    """
    Form for creating and updating DataAnalytics instances.
    """

    class Meta:
        model = DataAnalytics
        fields = "__all__"


class EditDataAnalyticsForm(forms.ModelForm):
    """
    Form for editing existing DataAnalytics instances.
    """

    class Meta:
        model = DataAnalytics
        fields = "__all__"


class AddDataAnalyticsForm(forms.ModelForm):
    """
    Form for adding new DataAnalytics instances.
    """

    class Meta:
        model = DataAnalytics
        fields = "__all__"


class ShiftForm(forms.ModelForm):
    """
    Form for creating and updating Shift instances.
    """

    class Meta:
        model = Shift
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating Category instances.
    """

    class Meta:
        model = Category
        fields = "__all__"


# New Forms for Adding, Editing, and Deleting Instances


class AddCategoryForm(forms.ModelForm):
    """
    Form for adding new Category instances.
    """

    class Meta:
        model = Category
        fields = "__all__"


class EditCategoryForm(forms.ModelForm):
    """
    Form for editing existing Category instances.
    """

    class Meta:
        model = Category
        fields = "__all__"


class DeleteCategoryForm(forms.ModelForm):
    """
    Form for deleting existing Category instances.
    """

    class Meta:
        model = Category
        fields = []


class AddShiftForm(forms.ModelForm):
    """
    Form for adding new Shift instances.
    """

    class Meta:
        model = Shift
        fields = "__all__"


class EditShiftForm(forms.ModelForm):
    """
    Form for editing existing Shift instances.
    """

    class Meta:
        model = Shift
        fields = "__all__"


class DeleteShiftForm(forms.ModelForm):
    """
    Form for deleting existing Shift instances.
    """

    class Meta:
        model = Shift
        fields = []


class DeleteProductForm(forms.ModelForm):
    """
    Form for deleting existing Product instances.
    """

    class Meta:
        model = Product
        fields = []


class DeleteSupplierForm(forms.ModelForm):
    """
    Form for deleting existing Supplier instances.
    """

    class Meta:
        model = Supplier
        fields = []


class DeleteEmployeeForm(forms.ModelForm):
    """
    Form for deleting existing Employee instances.
    """

    class Meta:
        model = Employee
        fields = []


class DeleteCustomerForm(forms.ModelForm):
    """
    Form for deleting existing Customer instances.
    """

    class Meta:
        model = Customer
        fields = []


class DeleteRevenueReportForm(forms.ModelForm):
    """
    Form for deleting existing RevenueReport instances.
    """

    class Meta:
        model = RevenueReport
        fields = []


class DeleteExpenseReportForm(forms.ModelForm):
    """
    Form for deleting existing ExpenseReport instances.
    """

    class Meta:
        model = ExpenseReport
        fields = []


class DeleteDataAnalyticsForm(forms.ModelForm):
    """
    Form for deleting existing DataAnalytics instances.
    """

    class Meta:
        model = DataAnalytics
        fields = []
