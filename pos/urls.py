from django.urls import path, include
from . import views

app_name = "pos"

urlpatterns = [
    path("", views.index, name="dashboard"),
    # Generic model URLs
    path("<str:model_name>/add/", views.add_view, name="add"),
    path("<str:model_name>/edit/<int:pk>/", views.edit_view, name="edit"),
    path("<str:model_name>/list/", views.generic_list_view, name="list"),
    path("<str:model_name>/detail/<int:pk>/", views.generic_detail_view, name="detail"),
    # Inventory URLs
    path(
        "inventory/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "Inventory"},
                    name="inventory_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "Inventory"},
                    name="inventory_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "inventory"},
                    name="inventory_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "inventory"},
                    name="inventory_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "inventory"},
                    name="inventory_delete",
                ),
            ]
        ),
    ),
    # Inventory Adjustment URLs
    path(
        "inventory_adjustment/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "InventoryAdjustment"},
                    name="inventory_adjustment_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "InventoryAdjustment"},
                    name="inventory_adjustment_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "inventory_adjustment"},
                    name="inventory_adjustment_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "inventory_adjustment"},
                    name="inventory_adjustment_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "inventory_adjustment"},
                    name="inventory_adjustment_delete",
                ),
            ]
        ),
    ),
    # Sales URLs
    path(
        "sales/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "Sale"},
                    name="sale_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "Sale"},
                    name="sale_detail",
                ),
                path(
                    "add/", 
                    views.add_view, 
                    {"model_name": "sale"}, 
                    name="sale_add"),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "sale"},
                    name="sale_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "sale"},
                    name="sale_delete",
                ),
            ]
        ),
    ),
    # Transactions URLs
    path(
        "transactions/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "Transaction"},
                    name="transaction_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "Transaction"},
                    name="transaction_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "transaction"},
                    name="transaction_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "transaction"},
                    name="transaction_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "transaction"},
                    name="transaction_delete",
                ),
            ]
        ),
    ),
    # Stock Alerts URLs
    path(
        "stock_alerts/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "StockAlert"},
                    name="stock_alert_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "StockAlert"},
                    name="stock_alert_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "stock_alert"},
                    name="stock_alert_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "stock_alert"},
                    name="stock_alert_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "stock_alert"},
                    name="stock_alert_delete",
                ),
            ]
        ),
    ),
    # Discounts URLs
    path(
        "discounts/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "Discount"},
                    name="discount_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "Discount"},
                    name="discount_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "discount"},
                    name="discount_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "discount"},
                    name="discount_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "discount"},
                    name="discount_delete",
                ),
            ]
        ),
    ),
    # Special Discounts URLs
    path(
        "special_discounts/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "SpecialDiscount"},
                    name="special_discount_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "SpecialDiscount"},
                    name="special_discount_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "special_discount"},
                    name="special_discount_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "special_discount"},
                    name="special_discount_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "special_discount"},
                    name="special_discount_delete",
                ),
            ]
        ),
    ),
    # Payments URLs
    path(
        "payments/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "Payment"},
                    name="payment_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "Payment"},
                    name="payment_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "payment"},
                    name="payment_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "payment"},
                    name="payment_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "payment"},
                    name="payment_delete",
                ),
            ]
        ),
    ),
    # Receipts URLs
    path(
        "receipts/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "Receipt"},
                    name="receipt_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "Receipt"},
                    name="receipt_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "receipt"},
                    name="receipt_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "receipt"},
                    name="receipt_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "receipt"},
                    name="receipt_delete",
                ),
            ]
        ),
    ),
    # Returns URLs
    path(
        "returns/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "Return"},
                    name="return_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "Return"},
                    name="return_detail",
                ),
                path(
                    "add/", views.add_view, {"model_name": "return"}, name="return_add"
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "return"},
                    name="return_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "return"},
                    name="return_delete",
                ),
            ]
        ),
    ),
    # Refunds URLs
    path(
        "refunds/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "Refund"},
                    name="refund_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "Refund"},
                    name="refund_detail",
                ),
                path(
                    "add/", views.add_view, {"model_name": "refund"}, name="refund_add"
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "refund"},
                    name="refund_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "refund"},
                    name="refund_delete",
                ),
            ]
        ),
    ),
    # Sales Analytics URLs
    path(
        "sales_analytics/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "SalesAnalytics"},
                    name="sales_analytics_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "SalesAnalytics"},
                    name="sales_analytics_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "sales_analytics"},
                    name="sales_analytics_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "sales_analytics"},
                    name="sales_analytics_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "sales_analytics"},
                    name="sales_analytics_delete",
                ),
            ]
        ),
    ),
    # Customer Analytics URLs
    path(
        "customer_analytics/",
        include(
            [
                path(
                    "list/",
                    views.generic_list_view,
                    {"model": "CustomerAnalytics"},
                    name="customer_analytics_list",
                ),
                path(
                    "detail/<int:pk>/",
                    views.generic_detail_view,
                    {"model": "CustomerAnalytics"},
                    name="customer_analytics_detail",
                ),
                path(
                    "add/",
                    views.add_view,
                    {"model_name": "customer_analytics"},
                    name="customer_analytics_add",
                ),
                path(
                    "edit/<int:pk>/",
                    views.edit_view,
                    {"model_name": "customer_analytics"},
                    name="customer_analytics_edit",
                ),
                path(
                    "delete/<int:pk>/",
                    views.delete_view,
                    {"model_name": "customer_analytics"},
                    name="customer_analytics_delete",
                ),
            ]
        ),
    ),
]