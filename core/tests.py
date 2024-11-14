from django.test import TestCase
from django.utils import timezone
from .models import Supplier, Category, Product, Customer, Employee, ExpenseReport, DataAnalytics, Shift, RevenueReport
from pos.models import Sale, Transaction, Inventory

class SupplierModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Test Supplier",
            contact_person="John Doe",
            address="123 Supplier St, Supplier City, Supplier Country",
            phone="1234567890",
            email="supplier@example.com",
            delivery_times="9 AM - 5 PM"
        )

    def test_supplier_str(self):
        self.assertEqual(str(self.supplier), "Test Supplier\nContact Person: John Doe\nPhone: 1234567890\nEmail: supplier@example.com\nDelivery Times: 9 AM - 5 PM")

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Test Category")

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.supplier = Supplier.objects.create(
            name="Test Supplier",
            contact_person="John Doe",
            address="123 Supplier St, Supplier City, Supplier Country",
            phone="1234567890",
            email="supplier@example.com",
            delivery_times="9 AM - 5 PM"
        )
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            description="Test Description",
            sku="TESTSKU",
            price=100.00,
            supplier=self.supplier,
            low_stock_threshold=10,
            barcode="1234567890123",
            expiration_date=timezone.now().date(),
            restock_date=timezone.now().date()
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product - TESTSKU")

    def test_product_stock(self):
        self.assertEqual(self.product.stock, 0)

    def test_product_update_stock(self):
        self.product.update_stock(50, "Initial stock")
        self.assertEqual(self.product.stock, 50)

    def test_product_is_low_stock(self):
        self.product.update_stock(5, "Low stock")
        self.assertTrue(self.product.is_low_stock())

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            phone_number="+1234567890",
            loyalty_points=100
        )

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Jane Doe (jane@example.com)")

    def test_add_loyalty_points(self):
        self.customer.add_loyalty_points(50)
        self.assertEqual(self.customer.loyalty_points, 150)

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="John Smith",
            phone_number="+1234567890",
            email="john@example.com",
            position="Manager",
            hire_date=timezone.now()
        )

    def test_employee_str(self):
        self.assertEqual(str(self.employee), f"Name: John Smith\nPhone: +1234567890\nEmail: john@example.com\nPosition: Manager\nHire Date: {self.employee.hire_date}\nShift Schedule: None")

class ExpenseReportModelTest(TestCase):
    def setUp(self):
        self.expense_report = ExpenseReport.objects.create(
            report_date=timezone.now(),
            description="Test Expense Report",
            total_expenses=1000.00
        )

    def test_expense_report_str(self):
        self.assertEqual(str(self.expense_report), f"Expense Report for {self.expense_report.report_date} : Test Expense Report - Total Expenses: 1000.00")

class DataAnalyticsModelTest(TestCase):
    def setUp(self):
        self.data_analytics = DataAnalytics.objects.create(
            report_date=timezone.now(),
            total_sales=10000.00,
            total_expenses=5000.00,
            total_profit=5000.00,
            metrics="Test Metrics",
            insights="Test Insights"
        )

    def test_data_analytics_str(self):
        self.assertEqual(str(self.data_analytics), f"Data Analytics for {self.data_analytics.report_date}\nTotal Sales: 10000.00\nTotal Expenses: 5000.00\nTotal Profit: 5000.00\nTop Selling Product: None\nTop Customer: None\nMetrics: Test Metrics\nInsights: Test Insights")

class ShiftModelTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            name="John Smith",
            phone_number="+1234567890",
            email="john@example.com",
            position="Manager",
            hire_date=timezone.now()
        )
        self.shift = Shift.objects.create(
            employee=self.employee,
            start_time=timezone.now(),
            end_time=timezone.now(),
            total_sales=1000.00,
            total_cash=500.00
        )

    def test_shift_str(self):
        self.assertEqual(str(self.shift), f"Shift for {self.employee.name}\nStart Time: {self.shift.start_time}\nEnd Time: {self.shift.end_time}\nTotal Sales: 1000.00\nTotal Cash: 500.00")

class RevenueReportModelTest(TestCase):
    def setUp(self):
        self.revenue_report = RevenueReport.objects.create(
            report_date=timezone.now(),
            total_revenue=10000.00,
            total_profit=5000.00,
            details={"detail": "Test Detail"}
        )

    def test_revenue_report_str(self):
        self.assertEqual(str(self.revenue_report), f"Revenue Report - {self.revenue_report.report_date.date()}")

        