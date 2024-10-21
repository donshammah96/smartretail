from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from pos.models import Sale, Payment, Transaction
from .models import Employee, Supplier, Product, Customer, RevenueReport, ExpenseReport, DataAnalytics, Shift , Category
from .forms import (
    ProductForm, SupplierForm, EmployeeForm, CustomerForm, RevenueReportForm, ExpenseReportForm, DataAnalyticsForm, ShiftForm, EditProductForm, EditSupplierForm, EditCustomerForm, EditEmployeeForm, EditRevenueReportForm, EditExpenseReportForm, EditDataAnalyticsForm, AddSaleForm, AddCustomerForm, AddProductForm, AddEmployeeForm, AddSupplierForm, AddExpenseForm, AddRevenueForm, AddDataAnalyticsForm, EditDataAnalyticsForm, CategoryForm
)

MODEL_FORM_MAPPING = {
    'product': (Product, ProductForm),
    'supplier': (Supplier, SupplierForm),
    'employee': (Employee, EmployeeForm),
    'eustomer': (Customer, CustomerForm),
    'revenue_report': (RevenueReport, RevenueReportForm),
    'expense_report': (ExpenseReport, ExpenseReportForm),
    'data_analytics': (DataAnalytics, DataAnalyticsForm),
    'shift': (Shift, ShiftForm),
}

MODEL_TEMPLATE_MAPPING = {
    'product': (Product, 'core/product_list.html', 'core/product_detail.html'),
    'category': (Category, 'core/category_list.html', 'core/category_detail.html'),
    'supplier': (Supplier, 'core/suppliers.html', 'core/supplier_detail.html'),
    'revenue_report': (RevenueReport, 'core/revenue_report.html', 'core/revenue_report_detail.html'),
    'expense_report': (ExpenseReport, 'core/expense_report.html', 'core/expense_report_detail.html'),
    'data_analytics': (DataAnalytics, 'core/data_analytics.html', 'core/data_analytics_detail.html'),
    'customer': (Customer, 'core/customers_list.html', 'core/customer_detail.html'),
    'employee': (Employee, 'core/employees_list.html', 'core/employee_detail.html'),
    'shift': (Shift, 'core/shifts_list.html', 'core/shift_detail.html'),
    'sale': (Sale, 'pos/sale_list.html', 'pos/sale_detail.html'),
}

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

def add_view(request, model_name):
    model, form_class = MODEL_FORM_MAPPING.get(model_name)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'success': True})
            return redirect(reverse(f'core:{model_name}_list'))
        else:
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = form_class()

    context = {
        'form': form,
        'model_name': model_name,
        'is_edit': False,
    }
    return render(request, 'core/add_edit.html', context)

def edit_view(request, model_name, pk):
    model, form_class = MODEL_FORM_MAPPING.get(model_name)
    instance = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'success': True})
            return redirect(reverse(f'core:{model_name}_list'))
        else:
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
        'model_name': model_name,
        'is_edit': True,
    }
    return render(request, 'core/add_edit.html', context)

def generic_list_view(request, model_name):
    model, list_template, _ = MODEL_TEMPLATE_MAPPING.get(model_name)
    objects = model.objects.all()
    return render(request, list_template, {model_name + 's': objects})

def generic_detail_view(request, model_name, pk):
    model, _, detail_template = MODEL_TEMPLATE_MAPPING.get(model_name)
    object = get_object_or_404(model, pk=pk)
    return render(request, detail_template, {model_name: object})

def about_view(request):
    return render(request, "core/about.html")

def contact_view(request):
    return render(request, "core/contact.html")