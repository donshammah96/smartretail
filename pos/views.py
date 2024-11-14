from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging
import json

from .services.mpesa_service import initiate_mpesa_payment
from .models import (
    Transaction,
    Discount,
    Sale,
    SpecialDiscount,
    StockAlert,
    SalesAnalytics,
    CustomerAnalytics,
    Payment,
    Receipt,
    Return,
    Refund,
    InventoryAdjustment,
    Inventory,
)
from .forms import (
    TransactionForm,
    DiscountForm,
    SpecialDiscountForm,
    StockAlertForm,
    SalesAnalyticsForm,
    CustomerAnalyticsForm,
    PaymentForm,
    ReceiptForm,
    ReturnForm,
    RefundForm,
    CreateTransactionForm,
    EditTransactionForm,
    EditSaleForm,
    SaleForm,
    InventoryAdjustmentForm,
    InventoryForm,
)


MODEL_FORM_MAPPING = {
    "transaction": (
        Transaction,
        TransactionForm,
        EditTransactionForm,
        CreateTransactionForm,
    ),
    "sale": (Sale, SaleForm, EditSaleForm),
    "discount": (Discount, DiscountForm),
    "special_discount": (SpecialDiscount, SpecialDiscountForm),
    "stock_alert": (StockAlert, StockAlertForm),
    "sales_analytics": (SalesAnalytics, SalesAnalyticsForm),
    "customer_analytics": (CustomerAnalytics, CustomerAnalyticsForm),
    "payment": (Payment, PaymentForm),
    "receipt": (Receipt, ReceiptForm),
    "return": (Return, ReturnForm),
    "refund": (Refund, RefundForm),
    "inventory": (Inventory, InventoryForm),
    "inventory_adjustment": (InventoryAdjustment, InventoryAdjustmentForm),
}

MODEL_TEMPLATE_MAPPING = {
    "transaction": (
        Transaction,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "discount": (
        Discount,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "special_discount": (
        SpecialDiscount,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "stock_alert": (
        StockAlert,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "sales_analytics": (
        SalesAnalytics,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "customer_analytics": (
        CustomerAnalytics,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "payment": (
        Payment,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "receipt": (
        Receipt,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "return": (
        Return,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "refund": (
        Refund,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "sale": (
        Sale,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "inventory": (
        Inventory,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
    "inventory_adjustment": (
        InventoryAdjustment,
        "pos/list_detail.html",
        "pos/add_edit.html",
    ),
}


# Get an instance of a logger
logger = logging.getLogger(
    "django"
)  # Use the 'django' logger or a custom one like 'custom_logger'


@login_required
def my_view(request):
    try:
        # Your code here...
        pass
    except Exception as e:
        # Log the error
        logger.error(f"An error occurred: {e}")


@login_required
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

    return render(request, "pos/dashboard.html", {"visits": visits})


@login_required
def add_view(request, model_name):
    """
    Generic view for adding new objects to the POS system.
    Handles form submission and AJAX requests.
    """
    try:
        model, form_class, _ = MODEL_FORM_MAPPING.get(model_name)
        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                form.save()
                if request.is_ajax():
                    return JsonResponse({"success": True})
                return redirect(reverse(f"pos:{model_name}_list"))
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
        return render(request, "pos/add_edit.html", context)

    except TypeError as e:
        logger.error(
            f"Invalid model name in add_view: {model_name}, Error: {e}"
        )  # Log the error
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect("pos:dashboard")


@login_required
def edit_view(request, model_name, pk):
    """
    Generic view for editing existing objects in the POS system.
    Handles form submission and AJAX requests.
    """
    try:
        model, form_class = MODEL_FORM_MAPPING.get(model_name)
        instance = get_object_or_404(model, pk=pk)
        if request.method == "POST":
            form = form_class(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                if request.is_ajax():
                    return JsonResponse({"success": True})
                return redirect(reverse(f"pos:{model_name}_list"))
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
        return render(request, "pos/add_edit.html", context)

    except TypeError as e:
        logger.error(
            f"Invalid model name in add_view: {model_name}, Error: {e}"
        )  # Log the error
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect("pos:dashboard")


@login_required
def generic_list_view(request, model_name):
    """
    Generic view for displaying a paginated list of objects in the POS system.
    """
    try:
        model, list_template, _ = MODEL_TEMPLATE_MAPPING.get(model_name)
        objects = model.objects.all()

        paginator = Paginator(objects, 10)
        page_number = request.GET.get("page")

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.get_page(1)
        # If page is not an integer, deliver first page.
        except EmptyPage:
            page_obj = paginator.get_page(
                paginator.num_pages
            )  # If page is out of range, deliver last page of results.

        context = {
            model_name + "_list": page_obj,
            "page_obj": page_obj,
            "model_name": model_name,
            "object_list": page_obj,  # Pass the Page object as 'object_list'
        }
        return render(request, list_template, context)

    except TypeError as e:
        logger.error(
            f"Invalid model name in generic_list_view: {model_name}, Error: {e}"
        )
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect("pos:dashboard")


@login_required
def generic_detail_view(request, model_name, pk):
    """
    Generic view for displaying details of an object in the POS system.
    """
    try:
        model, _, detail_template = MODEL_TEMPLATE_MAPPING.get(model_name)
        object = get_object_or_404(model, pk=pk)
        context = {
            model_name: object,
        }
        return render(request, detail_template, context)

    except TypeError as e:
        logger.error(
            f"Invalid model name in generic_detail_view: {model_name}, Error: {e}"
        )
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect("pos:dashboard")


@login_required
def delete_view(request, model_name, pk):
    """
    Generic view for deleting an object in the POS system.
    """
    try:
        model, _, _ = MODEL_TEMPLATE_MAPPING.get(model_name)
        object = get_object_or_404(model, pk=pk)

        object.delete()
        return redirect(reverse(f"pos:{model_name}_list"))

    except TypeError as e:
        logger.error(f"Invalid model name in delete_view: {model_name}, Error: {e}")
        messages.error(request, f"Invalid model name: {model_name}")
        return redirect("pos:dashboard")

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        checkout_request_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        callback_metadata = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])
        
        transaction_amount = None
        transaction_time = None
        mpesa_receipt_number = None

        for item in callback_metadata:
            if item.get('Name') == 'Amount':
                transaction_amount = item.get('Value')
            elif item.get('Name') == 'MpesaReceiptNumber':
                mpesa_receipt_number = item.get('Value')
            elif item.get('Name') == 'TransactionDate':
                transaction_time = item.get('Value')

        try:
            payment = Payment.objects.get(mpesa_transaction_id=checkout_request_id)
            if result_code == 0:
                payment.amount = transaction_amount
                payment.payment_date = transaction_time
                payment.mpesa_status = 'Completed'
                payment.mpesa_receipt_number = mpesa_receipt_number
            else:
                payment.mpesa_status = 'Failed'
            payment.save()
        except Payment.DoesNotExist:
            if result_code == 0:
                Payment.objects.create(
                    mpesa_transaction_id=checkout_request_id,
                    amount=transaction_amount,
                    payment_date=transaction_time,
                    method='M-Pesa',
                    mpesa_status='Completed',
                    mpesa_receipt_number=mpesa_receipt_number
                )
            else:
                Payment.objects.create(
                    mpesa_transaction_id=checkout_request_id,
                    amount=transaction_amount,
                    payment_date=transaction_time,
                    method='M-Pesa',
                    mpesa_status='Failed'
                )

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
    return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid Request Method'})

@csrf_exempt
def mpesa_confirmation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data.get('TransID')
        transaction_amount = data.get('TransAmount')
        transaction_time = data.get('TransTime')
        phone_number = data.get('MSISDN')
        account_reference = data.get('BillRefNumber')

        try:
            payment = Payment.objects.get(mpesa_transaction_id=transaction_id)
            payment.amount = transaction_amount
            payment.payment_date = transaction_time
            payment.mpesa_status = 'Completed'
            payment.save()
        except Payment.DoesNotExist:
            Payment.objects.create(
                mpesa_transaction_id=transaction_id,
                amount=transaction_amount,
                payment_date=transaction_time,
                method='M-Pesa',
                mpesa_status='Completed',
                phone_number=phone_number,
                account_reference=account_reference
            )

        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
    return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid Request Method'})

@login_required
def initiate_payment(request, transaction_id):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        amount = request.POST['amount']
        transaction_desc = request.POST['transaction_desc']
        account_reference = request.POST['account_reference']

        response = initiate_mpesa_payment(phone_number, amount, account_reference, transaction_desc)
        if response.get('ResponseCode') == '0':
            payment = Payment.objects.create(
                transaction_id=transaction_id,
                method='M-Pesa',
                amount=amount,
                mpesa_transaction_id=response.get('CheckoutRequestID'),
                mpesa_status='Pending'
            )
            messages.success(request, 'Payment initiated successfully.')
            return redirect('payment_success')
        else:
            messages.error(request, 'Payment initiation failed.')
            return redirect('payment_failure')

    return render(request, 'initiate_payment.html')