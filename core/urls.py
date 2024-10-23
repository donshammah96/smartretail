from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.index, name="dashboard"),
    path('<str:model_name>/add/', views.add_view, name='add'),
    path('<str:model_name>/edit/<int:pk>/', views.edit_view, name='edit'),
    path('<str:model_name>/list/', views.generic_list_view, name='list'),
    path('<str:model_name>/detail/<int:pk>/', views.generic_detail_view, name='detail'),
    # Products URLs
    path('products/', include([
        path('', views.generic_list_view, {'model': 'Product'}, name='product_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'Product'}, name='product_detail'),
        path('add/', views.add_view, {'model_name': 'product'}, name='product_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'product'}, name='product_edit'),
    ])),

    # Categories URLs
    path('categories/', include([
        path('', views.generic_list_view, {'model': 'Category'}, name='category_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'Category'}, name='category_detail'),
        path('add/', views.add_view, {'model_name': 'category'}, name='category_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'category'}, name='category_edit'),
    ])),

    # Suppliers URLs
    path('suppliers/', include([
        path('', views.generic_list_view, {'model': 'Supplier'}, name='supplier_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'Supplier'}, name='supplier_detail'),
        path('add/', views.add_view, {'model_name': 'supplier'}, name='supplier_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'supplier'}, name='supplier_edit'),
    ])),

    # Revenue Reports URLs
    path('revenue_reports/', include([
        path('', views.generic_list_view, {'model': 'RevenueReport'}, name='revenue_report_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'RevenueReport'}, name='revenue_report_detail'),
        path('add/', views.add_view, {'model_name': 'revenue_report'}, name='revenue_report_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'revenue_report'}, name='revenue_report_edit'),
    ])),

    # Expense Reports URLs
    path('expense_reports/', include([
        path('', views.generic_list_view, {'model': 'ExpenseReport'}, name='expense_report_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'ExpenseReport'}, name='expense_report_detail'),
        path('add/', views.add_view, {'model_name': 'expense_report'}, name='expense_report_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'expense_report'}, name='expense_report_edit'),
    ])),

    # Data Analytics URLs
    path('data_analytics/', include([
        path('', views.generic_list_view, {'model': 'DataAnalytics'}, name='data_analytics_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'DataAnalytics'}, name='data_analytics_detail'),
        path('add/', views.add_view, {'model_name': 'data_analytics'}, name='data_analytics_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'data_analytics'}, name='data_analytics_edit'),
    ])),

    # Customers URLs
    path('customers/', include([
        path('', views.generic_list_view, {'model': 'Customer'}, name='customers_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'Customer'}, name='customer_detail'),
        path('add/', views.add_view, {'model_name': 'customer'}, name='customer_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'customer'}, name='customer_edit'),
    ])),

    # Employees URLs
    path('employees/', include([
        path('', views.generic_list_view, {'model': 'Employee'}, name='employees_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'Employee'}, name='employee_detail'),
        path('add/', views.add_view, {'model_name': 'employee'}, name='employee_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'employee'}, name='employee_edit'),
    ])),

    # Shifts URLs
    path('shifts/', include([
        path('', views.generic_list_view, {'model': 'Shift'}, name='shift_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'Shift'}, name='shift_detail'),
        path('add/', views.add_view, {'model_name': 'shift'}, name='shift_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'shift'}, name='shift_edit'),
    ])),

    # Stocks URLs
    path('stocks/', include([
        path('', views.generic_list_view, {'model': 'Stock'}, name='stock_list'),
        path('<int:pk>/', views.generic_detail_view, {'model': 'Stock'}, name='stock_detail'),
        path('add/', views.add_view, {'model_name': 'stock'}, name='stock_add'),
        path('edit/<int:pk>/', views.edit_view, {'model_name': 'stock'}, name='stock_edit'),
    ])),

    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

    # Include URLs from other apps
    path('pos/', include('pos.urls')),
    path('users/', include('users.urls')),
]
