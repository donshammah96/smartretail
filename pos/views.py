from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django import forms
from django.utils import timezone
from .models import (
    Transaction, Discount, Sale, SpecialDiscount, StockAlert, SalesAnalytics, CustomerAnalytics, 
    Payment, Receipt, Return, Refund, InventoryAdjustment, Inventory
)
from .forms import (
   TransactionForm, DiscountForm, SpecialDiscountForm, StockAlertForm, SalesAnalyticsForm, CustomerAnalyticsForm, 
    PaymentForm, ReceiptForm, ReturnForm, RefundForm, CreateTransactionForm, EditTransactionForm, EditSaleForm, SaleForm, InventoryAdjustmentForm, InventoryForm
)


MODEL_FORM_MAPPING = {
    'transaction': (Transaction, TransactionForm),
    'sale': (Sale, SaleForm),
    'discount': (Discount, DiscountForm),
    'special_discount': (SpecialDiscount, SpecialDiscountForm),
    'stock_alert': (StockAlert, StockAlertForm),
    'sales_analytics': (SalesAnalytics, SalesAnalyticsForm),
    'customer_analytics': (CustomerAnalytics, CustomerAnalyticsForm),
    'payment': (Payment, PaymentForm),
    'receipt': (Receipt, ReceiptForm),
    'return': (Return, ReturnForm),
    'refund': (Refund, RefundForm),
    'inventory': (Inventory, InventoryForm),
    'inventory_adjustment': (InventoryAdjustment, InventoryAdjustmentForm),
}

MODEL_TEMPLATE_MAPPING = {
    'transaction': (Transaction, 'pos/transaction_list.html', 'pos/transaction_detail.html'),
    'discount': (Discount, 'pos/discount_list.html', 'pos/discount_detail.html'),
    'special_discount': (SpecialDiscount, 'pos/special_discount_list.html', 'pos/special_discount_detail.html'),
    'stock_alert': (StockAlert, 'pos/stock_alert_list.html', 'pos/stock_alert_detail.html'),
    'sales_analytics': (SalesAnalytics, 'pos/sales_analytics_list.html', 'pos/sales_analytics_detail.html'),
    'customer_analytics': (CustomerAnalytics, 'pos/customer_analytics_list.html', 'pos/customer_analytics_detail.html'),
    'payment': (Payment, 'pos/payment_list.html', 'pos/payment_detail.html'),
    'receipt': (Receipt, 'pos/receipt_list.html', 'pos/receipt_detail.html'),
    'return': (Return, 'pos/return_list.html', 'pos/return_detail.html'),
    'refund': (Refund, 'pos/refund_list.html', 'pos/refund_detail.html'),
    'sale': (Sale, 'pos/sale_list.html', 'pos/sale_detail.html'),
    'inventory': (Inventory, 'pos/inventory_list.html', 'pos/inventory_detail.html'),
    'inventory_adjustment': (InventoryAdjustment, 'pos/inventory_adjustment_list.html', 'pos/inventory_adjustment_detail.html'),
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

    return render(request, "pos/dashboard.html", {'visits': visits})

def add_view(request, model_name):
    model, form_class = MODEL_FORM_MAPPING.get(model_name)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'success': True})
            return redirect(reverse(f'pos:{model_name}_list'))
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
    return render(request, 'pos/add_edit.html', context)

def edit_view(request, model_name, pk):
    model, form_class = MODEL_FORM_MAPPING.get(model_name)
    instance = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'success': True})
            return redirect(reverse(f'pos:{model_name}_list'))
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
    return render(request, 'pos/add_edit.html', context)

def generic_list_view(request, model_name):
    model, list_template, _ = MODEL_TEMPLATE_MAPPING.get(model_name)
    objects = model.objects.all()
    return render(request, list_template, {model_name + 's': objects})

def generic_detail_view(request, model_name, pk):
    model, _, detail_template = MODEL_TEMPLATE_MAPPING.get(model_name)
    object = get_object_or_404(model, pk=pk)
    return render(request, detail_template, {model_name: object})