from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.contrib import messages
from pos.models import Sale
import logging

from .models import (
    Employee,
    Supplier,
    Product,
    Customer,
    RevenueReport,
    ExpenseReport,
    DataAnalytics,
    Shift,
    Category,
)
from .forms import (
    ProductForm,
    SupplierForm,
    EmployeeForm,
    CustomerForm,
    RevenueReportForm,
    ExpenseReportForm,
    DataAnalyticsForm,
    ShiftForm,
    EditProductForm,
    EditSupplierForm,
    EditCustomerForm,
    EditEmployeeForm,
    EditRevenueReportForm,
    EditExpenseReportForm,
    EditDataAnalyticsForm,
    AddSaleForm,
    AddCustomerForm,
    AddProductForm,
    AddEmployeeForm,
    AddSupplierForm,
    AddExpenseForm,
    AddRevenueForm,
    AddDataAnalyticsForm,
    CategoryForm,
    AddCategoryForm,
    EditCategoryForm,
    DeleteCategoryForm,
    AddShiftForm,
    EditShiftForm,
    DeleteShiftForm,
    DeleteProductForm,
    DeleteSupplierForm,
    DeleteEmployeeForm,
    DeleteCustomerForm,
    DeleteRevenueReportForm,
    DeleteExpenseReportForm,
    DeleteDataAnalyticsForm,
)

# Mapping for Add Forms
ADD_FORM_MAPPING = {
    "product": AddProductForm,
    "supplier": AddSupplierForm,
    "employee": AddEmployeeForm,
    "customer": AddCustomerForm,
    "revenue_report": AddRevenueForm,
    "expense_report": AddExpenseForm,
    "data_analytics": AddDataAnalyticsForm,
    "shift": AddShiftForm,
    "category": AddCategoryForm,
}

# Mapping for Edit Forms
EDIT_FORM_MAPPING = {
    "product": EditProductForm,
    "supplier": EditSupplierForm,
    "employee": EditEmployeeForm,
    "customer": EditCustomerForm,
    "revenue_report": EditRevenueReportForm,
    "expense_report": EditExpenseReportForm,
    "data_analytics": EditDataAnalyticsForm,
    "shift": EditShiftForm,
    "category": EditCategoryForm,
}

# Mapping for Delete Forms
DELETE_FORM_MAPPING = {
    "product": (Product, DeleteProductForm),
    "supplier": (Supplier, DeleteSupplierForm),
    "employee": (Employee, DeleteEmployeeForm),
    "customer": (Customer, DeleteCustomerForm),
    "revenue_report": (RevenueReport, DeleteRevenueReportForm),
    "expense_report": (ExpenseReport, DeleteExpenseReportForm),
    "data_analytics": (DataAnalytics, DeleteDataAnalyticsForm),
    "shift": (Shift, DeleteShiftForm),
    "category": (Category, DeleteCategoryForm),
}

# Model and Form Mapping
MODEL_FORM_MAPPING = {
    "product": (Product, ProductForm, EditProductForm),
    "supplier": (Supplier, SupplierForm, EditSupplierForm),
    "employee": (Employee, EmployeeForm, EditEmployeeForm),
    "customer": (Customer, CustomerForm, EditCustomerForm),
    "revenue_report": (RevenueReport, RevenueReportForm, EditRevenueReportForm),
    "expense_report": (ExpenseReport, ExpenseReportForm, EditExpenseReportForm),
    "data_analytics": (DataAnalytics, DataAnalyticsForm, EditDataAnalyticsForm),
    "shift": (Shift, ShiftForm, EditShiftForm),
    "category": (Category, CategoryForm, EditCategoryForm),
}

MODEL_TEMPLATE_MAPPING = {
    "product": (
        Product, 
        "core/list_detail.html", 
        "core/add_edit.html"
        ),
    "category": (
        Category, 
        "core/list_detail.html", 
        "core/add_edit.html"
        ),
    "supplier": (
        Supplier, 
        "core/list_detail.html", 
        "core/add_edit.html"
        ),
    "revenue_report": (
        RevenueReport,
        "core/list_detail.html", 
        "core/add_edit.html"
    ),
    "expense_report": (
        ExpenseReport,
        "core/list_detail.html", 
        "core/add_edit.html"
    ),
    "data_analytics": (
        DataAnalytics,
        "core/list_detail.html", 
        "core/add_edit.html"
    ),
    "customer": (
        Customer, 
        "core/list_detail.html", 
        "core/add_edit.html"
        ),
    "employee": (
        Employee, 
        "core/list_detail.html", 
        "core/add_edit.html"
        ),
    "shift": (
        Shift, 
        "core/list_detail.html", 
        "core/add_edit.html"
    ),
    "sale": (
        Sale, 
        "core/list_detail.html", 
        "core/add_edit.html"
        ),
}

# Get an instance of a logger
logger = logging.getLogger(
    "django"
)  # Use the 'django' logger or a custom one like 'custom_logger'


def my_view(request):
    try:
        # Your code here...
        pass
    except Exception as e:
        # Log the error
        logger.error(f"An error occurred: {e}")

def index(request):
    # Check if the session key 'visits' exists
    if "visits" in request.session:
        # Increment the number of visits
        request.session["visits"] += 1
    else:
        # Initialize the number of visits
        request.session["visits"] = 1

    # Retrieve the number of visits from the session
    visits = request.session["visits"]

    return render(request, "core/dashboard.html", {"visits": visits})

def add_view(request, model_name):
    """
    Generic view for adding new objects to the CORE system.
    Handles form submission and AJAX requests.
    """
    try:
        form_class = ADD_FORM_MAPPING.get(model_name)  # Get only the form class
        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                new_object = form.save()
                if request.is_ajax():
                    return JsonResponse({"success": True, 'pk': new_object.pk})
                return redirect(reverse(f"core:{model_name}_detail", kwargs={'pk': new_object.pk}))
            else:
                if request.is_ajax():
                    return JsonResponse({"success": False, "errors": form.errors})
        else:
            form = form_class()

        context = {
            "form": form,
            "model_name": model_name,
            "is_edit": False,
        }
        return render(request, "core/add_edit.html", context)

    except TypeError as e:
        logger.error(f"Invalid model name in add_view: {model_name}, Error: {e}")
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect('core:dashboard')
    
def edit_view(request, model_name, pk):
    """
    Generic view for editing existing objects in the CORE system.
    Handles form submission and AJAX requests.
    """
    try:
        model, form_class = EDIT_FORM_MAPPING.get(model_name)  # Get both model and form class
        instance = get_object_or_404(model, pk=pk)
        if request.method == "POST":
            form = form_class(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                if request.is_ajax():
                    return JsonResponse({"success": True})
                return redirect(reverse(f"core:{model_name}_list"))
            else:
                if request.is_ajax():
                    return JsonResponse({"success": False, "errors": form.errors})
        else:
            form = form_class(instance=instance)

        context = {
            "form": form,
            "model_name": model_name,
            "is_edit": True,
        }
        return render(request, "core/add_edit.html", context)

    except TypeError as e:
        logger.error(f"Invalid model name in edit_view: {model_name}, Error: {e}")
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect('core:dashboard')
    
def generic_list_view(request, model_name):
    """
    Generic view for displaying a paginated list of objects in the POS system.
    """
    try:
        model, list_template, _ = MODEL_TEMPLATE_MAPPING.get(model_name)
        objects = model.objects.all()

        paginator = Paginator(objects, 10) 
        page_number = request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
  # If page is not an integer, deliver first page.
        except EmptyPage:
            page_obj = paginator.get_page(paginator.num_pages)  # If page is out of range, deliver last page of results.

        context = {
            model_name + '_list': page_obj,
            'page_obj': page_obj,
            'model_name': model_name,
            'object_list': page_obj,  # Pass the Page object as 'object_list'
        }
        return render(request, list_template, context)

    except TypeError as e:
        logger.error(f"Invalid model name in generic_list_view: {model_name}, Error: {e}")
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect('core:dashboard')

def generic_detail_view(request, model_name, pk):
    """
    Generic view for displaying details of an object in the CORE system.
    """
    try:
        model, _, detail_template = MODEL_TEMPLATE_MAPPING.get(model_name)
        object = get_object_or_404(model, pk=pk)
        context = {
            model_name: object,
        }
        return render(request, detail_template, context)

    except TypeError as e:
        logger.error(f"Invalid model name in generic_detail_view: {model_name}, Error: {e}")
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect('core:dashboard')

def about_view(request):
    """
    View for the about page.
    """
    return render(request, "core/about.html")

def contact_view(request):
    """
    View for the contact page.
    """
    return render(request, "core/contact.html")

def delete_view(request, model_name, pk):
    """
    Generic view for deleting an object in the CORE system.
    """
    try:
        model, _ = MODEL_FORM_MAPPING.get(model_name)
        object = get_object_or_404(model, pk=pk)
        object.delete()
        messages.success(request, f"{model_name.capitalize()} deleted successfully.")
        return redirect(reverse(f"core:{model_name}_list"))  # Redirect to the list view

    except TypeError as e:
        logger.error(f"Invalid model name in delete_view: {model_name}, Error: {e}")
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect('core:dashboard')