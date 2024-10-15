from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.create_transaction, name='create_transaction'),
    path('sales/add/', views.add_sale, name='add_sale'),
    path('sales/', views.add_sale, name='sales'),
    path('customers/', views.customer_list, name='customers_list'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/update_stock/', views.update_stock, name='update_stock'),
    path('stock/', views.stock, name='stock'),
    path('employees/', views.employees_list, name='employees_list'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('revenue_report/', views.revenue_report, name='revenue_report'),
    path('revenue_report/add/', views.add_revenue, name='add_revenue'),
    path('expense_report/', views.expense_report, name='expense_report'),
    path('expense_report/add/', views.add_expense, name='add_expense'),
    path('data_analytics/', views.data_analytics, name='data_analytics'),
]