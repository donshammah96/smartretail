from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Employee, Supplier, Product, Customer, RevenueReport, ExpenseReport, DataAnalytics, Shift

# Define forms for Employee and Supplier
class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'email', 'phone', 'hire_date', 'shift_schedule']

class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'phone', 'email', 'delivery_times']

class AddSaleForm(forms.Form):
    product_id = forms.ChoiceField(choices=[])  # Populate choices dynamically in the view
    quantity = forms.IntegerField(min_value=1)

class CreateTransactionForm(forms.Form):
    # Define your form fields here
    pass

class AddCustomerForm(forms.Form):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'loyalty_points']

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'price', 'stock', 'supplier', 'low_stock_threshold', 'barcode']

class UpdateStockForm(forms.Form):
    product_id = forms.ChoiceField(choices=[])  # Populate choices dynamically in the view
    quantity = forms.IntegerField(min_value=1)

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseReport
        fields = ['description', 'total_expenses', 'report_date']

class AddRevenueForm(forms.ModelForm):
    class Meta:
        model = RevenueReport
        fields = ['total_revenue', 'total_profit', 'report_date']

def index(request):
    # Check if the session key 'visits' exists
    if 'visits' in request.session:
        # Increment the number of visits
        request.session['visits'] += 1
    else:
        # Initialize the number of visits
        request.session['visits'] = 1

    # Retrieve the number of visits from the session
    visits = request.session['visits']

    return render(request, "core/dashboard.html", {'visits': visits})

def add_sale(request):
    if request.method == "POST":
        form = AddSaleForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, pk=product_id)
            product.update_stock(-quantity)
            return HttpResponseRedirect(reverse("core:transaction_list"))
    else:
        form = AddSaleForm()
        form.fields['product_id'].choices = [(product.id, product.name) for product in Product.objects.all()]
    return render(request, "core/add_sale.html", {'form': form})

def create_transaction(request):
    if request.method == "POST":
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            # Handle form submission logic here
            transaction = form.cleaned_data
            # Add the new transaction to the session
            request.session['transactions_list'] = request.session.get('transactions_list', []) + [transaction]
            return HttpResponseRedirect(reverse("core:transaction_list"))
    else:
        form = CreateTransactionForm()
    return render(request, "core/create_transaction.html", {'form': form})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "core/customers_list.html", {"customers": customers})

def product_list(request):
    products = Product.objects.all()
    return render(request, "core/product_list.html", {
        "products": products
        })

def transaction_list(request):
    transactions = request.session.get('transactions_list', [])  # Replace with actual data fetching logic
    return render(request, "core/transaction_list.html", {"transactions": transactions})

def update_stock(request):
    if request.method == "POST":
        form = UpdateStockForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, pk=product_id)
            product.update_stock(quantity)
            return HttpResponseRedirect(reverse("core:product_list"))
    else:
        form = UpdateStockForm()
        form.fields['product_id'].choices = [(product.id, product.name) for product in Product.objects.all()]
    return render(request, "core/update_stock.html", {'form': form})

def stock(request):
    products = Product.objects.all()
    return render(request, "core/stock.html", {"products": products})

def add_customer(request):
    if request.method == "POST":
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:customer_list"))
    else:
        form = AddCustomerForm()
    return render(request, "core/add_customer.html", {"form": form})

def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:product_list"))
    else:
        form = AddProductForm()
    return render(request, "core/add_product.html", {"form": form})

def add_employee(request):
    if request.method == "POST":
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:employees_list"))
    else:
        form = AddEmployeeForm()
    return render(request, "core/add_employee.html", {"form": form})

def employees_list(request):
    employees = Employee.objects.all()
    return render(request, "core/employees_list.html", {"employees": employees})

def add_supplier(request):
    if request.method == "POST":
        form = AddSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:suppliers"))
    else:
        form = AddSupplierForm()
    return render(request, "core/add_supplier.html", {"form": form})

def suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, "core/suppliers.html", {
        "suppliers": suppliers
        })

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    return render(request, 'core/supplier_detail.html', {'supplier': supplier})

def revenue_report(request):
    revenue_data = RevenueReport.objects.all()
    return render(request, "core/revenue_report.html", {"revenue_data": revenue_data})

def expense_report(request):
    expense_data = ExpenseReport.objects.all()
    return render(request, "core/expense_report.html", {"expense_data": expense_data})

def data_analytics(request):
    analytics_data = DataAnalytics.objects.all()
    return render(request, "core/data_analytics.html", {"analytics_data": analytics_data})

def add_expense(request):
    if request.method == "POST":
        form = AddExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:expense_report"))
    else:
        form = AddExpenseForm()
    return render(request, "core/add_expense.html", {"form": form})

def add_revenue(request):
    if request.method == "POST":
        form = AddRevenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("core:revenue_report"))
    else:
        form = AddRevenueForm()
    return render(request, "core/add_revenue.html", {"form": form})