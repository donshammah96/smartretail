from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError, DatabaseError
from django.utils.decorators import method_decorator
from datetime import datetime
from django.db.models import Sum
import logging
import json
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.cache import cache
from .models import UserStats
from django.core.exceptions import ObjectDoesNotExist


# Mixin to fetch role-based stats data
class RoleStatsMixin:
    def get_stats(self):
        # Identify the role of the current user
        user_role = self.request.user.role
        # Define a unique cache key based on the user role
        cache_key = f"{user_role}_stats"
        # Try to retrieve the stats from the cache
        stats = cache.get(cache_key)

        # If cache is empty, fetch stats from the database
        if not stats:
            if user_role == "admin":
                stats = self.get_admin_stats()
            elif user_role == "manager":
                stats = self.get_manager_stats()
            elif user_role == "employee":
                stats = self.get_employee_stats()
            # Store stats in the cache for 15 minutes
            cache.set(cache_key, stats, timeout=60 * 15)

        return stats

    def get_admin_stats(self):
        # Fetch data relevant to admin users
        return UserStats.objects.admin_stats()

    def get_manager_stats(self):
        # Fetch data relevant to manager users
        return UserStats.objects.manager_stats()

    def get_employee_stats(self):
        # Fetch data relevant to employee users
        return UserStats.objects.employee_stats()


# Admin Dashboard
class AdminDashboardView(LoginRequiredMixin, RoleStatsMixin, TemplateView):
    template_name = "users/admin_dashboard.html"

    def get_context_data(self, **kwargs):
        # Add admin-specific stats to the context
        context = super().get_context_data(**kwargs)
        context["stats"] = self.get_stats()
        context['chart_data'] = self.get_chart_data()
        return context

    def get_chart_data(self):
        # Calculate or retrieve chart data for managers
        return {"labels": ["Jan", "Feb", "Mar", "Apr"], "data": [10, 20, 30, 40]}
    
# Manager Dashboard
class ManagerDashboardView(LoginRequiredMixin, RoleStatsMixin, TemplateView):
    template_name = "users/manager_dashboard.html"

    def get_context_data(self, **kwargs):
        # Add manager-specific stats and chart data to the context
        context = super().get_context_data(**kwargs)
        context["stats"] = self.get_stats()
        context["chart_data"] = self.get_chart_data()
        return context

    def get_chart_data(self):
        # Calculate or retrieve chart data for managers
        return {"labels": ["Jan", "Feb", "Mar", "Apr"], "data": [10, 20, 30, 40]}


# Employee Dashboard
class EmployeeDashboardView(LoginRequiredMixin, RoleStatsMixin, TemplateView):
    template_name = "users/employee_dashboard.html"

    def get_context_data(self, **kwargs):
        # Add employee-specific chart data to the context
        context = super().get_context_data(**kwargs)
        context["stats"] = self.get_stats()
        context["chart_data"] = self.get_chart_data()
        return context

    def get_chart_data(self):
        # Calculate or retrieve chart data for employees
        return {"labels": ["Jan", "Feb", "Mar", "Apr"], "data": [15, 25, 35, 45]}


# Get an instance of a logger
logger = logging.getLogger(
    "django"
)  # Use the 'django' logger or a custom one like 'custom_logger'


def home(request):
    """
    View for the homepage.
    Redirects logged-in users to the main dashboard.
    """
    if request.user.is_authenticated:
        user_role = request.user.role
        if user_role == 'admin':
            return redirect('users:admin_dashboard')
        elif user_role == 'manager':
            return redirect('users:manager_dashboard')
        elif user_role == 'employee':
            return redirect('users:employee_dashboard')
        else:
            return redirect('users:dashboard')

    # Render the home page for non-authenticated users
    context = {
        "user": request.user,
    }
    return render(request, "users/home.html", context)


def my_view(request):
    try:
        # Your code here...
        pass
    except Exception as e:
        # Log the error
        logger.error(f"An error occurred: {e}")


from .forms import (
    UserLoginForm,
    UserRegisterForm,
    UserEditForm,
    CustomPasswordChangeForm,
    UserDeleteForm,
)
from .models import CustomUser, Employee, UserActivity, TrainingResource, Notification
from pos.models import Sale, Inventory

# Custom decorator for checking user roles (supports list or single role)


def role_required(roles):
    if not isinstance(roles, list):
        roles = [roles]

    def decorator(view_func):
        @login_required  # This ensures that a session must be active
        @user_passes_test(lambda user: user.role in roles)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


@login_required
def dashboard(request):
    user_role = request.user.role  # Assuming you have a role attribute on your user model

    if user_role == 'admin':
        view = AdminDashboardView.as_view()
    elif user_role == 'manager':
        view = ManagerDashboardView.as_view()
    elif user_role == 'employee':
        view = EmployeeDashboardView.as_view()
    else:
        return redirect('users:home')

    return view(request)

@login_required
@role_required(["employee", "admin", "manager"])
def sales_overview_employee(request):
    sales = Sale.objects.filter(employee=request.user).order_by("-date")
    return render(request, "users/sales_overview.html", {"sales": sales})


@login_required
@role_required("admin")
def sales_overview_admin(request):
    sales = Sale.objects.all().order_by("-date")
    return render(request, "users/sales_overview.html", {"sales": sales})


@login_required
@role_required("employee")
def inventory_check_employee(request):
    inventory = Inventory.objects.filter(employee=request.user)
    return render(request, "users/inventory_check.html", {"inventory": inventory})


@login_required
@role_required("admin")
def inventory_check_admin(request):
    inventory = Inventory.objects.all()
    return render(request, "users/inventory_check.html", {"inventory": inventory})


@login_required
@role_required("employee")
def training_resources_employee(request):
    resources = TrainingResource.objects.filter(employee=request.user)
    return render(request, "users/training_resources.html", {"resources": resources})


@login_required
@role_required("admin")
def training_resources_admin(request):
    resources = TrainingResource.objects.all()
    return render(request, "users/training_resources.html", {"resources": resources})


@login_required
@role_required("employee")
def notifications_employee(request):
    notifications = Notification.objects.filter(employee=request.user).order_by("-date")
    return render(request, "users/notifications.html", {"notifications": notifications})


@login_required
@role_required("admin")
def notifications_admin(request):
    notifications = Notification.objects.all().order_by("-date")
    return render(request, "users/notifications.html", {"notifications": notifications})


@role_required(["admin", "manager"])
def employee_list(request):
    employees = CustomUser.objects.filter(role="employee").select_related("employee")
    return render(
        request,
        "core/list_detail.html",
        {"employees": employees, "model_name": "employee"},
    )


@role_required(["admin", "manager"])
def employee_profile(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    profile = get_object_or_404(Employee, user=employee)
    return render(
        request,
        "core:detail' model_name='employee' pk=employee.id %",
        {"employee": employee, "profile": profile},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("users:dashboard")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  # This handles session setup
                log_user_activity(user, "logged in")
                return redirect("users:dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Error processing your login form.")
    else:
        form = UserLoginForm()

    return render(request, "users/login.html", {"form": form})


def register_view(request):
    """
    View for user registration.
    Handles form submission and redirects based on user role.
    """
    if request.user.is_authenticated:
        return redirect("users:dashboard")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                log_user_activity(user, "registered")
                messages.success(request, "Registration successful.")

                # Redirect based on user role
                if user.role == "employee":
                    return redirect("users:employee_dashboard")
                elif user.role == "manager":
                    return redirect("users:manager_dashboard")
                elif user.role == "admin":
                    return redirect("users:admin_dashboard")
                else:
                    return redirect("users:dashboard")  # Default redirect

            except IntegrityError:
                messages.error(request, "Error during registration. Please try again.")
        else:
            messages.error(request, "Error processing your registration form.")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    log_user_activity(request.user, "logged out")
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("users:login")


@role_required("manager")
def user_performance_report(request):
    employees = Employee.objects.select_related("user")

    for employee in employees:
        employee.total_sales = calculate_total_sales(employee)
        employee.average_transaction_value = calculate_average_transaction_value(
            employee
        )
        employee.performance_score = calculate_performance_score(employee)

    paginator = Paginator(employees, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "users/user_performance_report.html", {"page_obj": page_obj})


@role_required("manager")
def user_activity_report(request):
    activities = UserActivity.objects.all().order_by("-timestamp")

    paginator = Paginator(activities, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "users/user_activity_report.html", {"page_obj": page_obj})


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Profile updated successfully.")
            except DatabaseError:
                messages.error(request, "Error updating your profile.")
            return redirect("users:profile")
        else:
            messages.error(request, "Error updating your profile.")
    else:
        form = UserEditForm(instance=request.user)

    return render(request, "users/edit_profile.html", {"form": form})


def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
            except DatabaseError:
                messages.error(request, "Error changing your password.")
            return redirect("users:profile")
        else:
            messages.error(request, "Error changing your password.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, "users/change_password.html", {"form": form})


@role_required("admin")
def delete_profile(request):
    if request.method == "POST":
        form = UserDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data["confirm"]:
            try:
                request.user.delete()
                messages.success(request, "Profile deleted successfully.")
                return redirect("users:login")
            except DatabaseError:
                messages.error(request, "Error deleting your profile.")
        else:
            messages.error(request, "Please confirm the deletion.")
    else:
        form = UserDeleteForm()

    return render(request, "users/delete_profile.html", {"form": form})


@role_required("manager")
def user_performance_report(request):
    employees = Employee.objects.all()  # Get all employees

    # Calculate performance metrics for each employee
    for employee in employees:
        employee.total_sales = calculate_total_sales(employee)
        employee.average_transaction_value = calculate_average_transaction_value(
            employee
        )
        employee.performance_score = calculate_performance_score(employee)

    # Paginate the employees list
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "users/user_performance_report.html", {"page_obj": page_obj})


def calculate_total_sales(employee):
    """Calculate the total sales made by an employee."""
    sales = Sale.objects.filter(
        employee__user=employee.user
    )  # Access Sale through employee.user
    total_sales = sum(sale.final_price for sale in sales)
    return total_sales


def calculate_average_transaction_value(employee):
    """Calculate the average transaction value for an employee."""
    sales = Sale.objects.filter(
        employee__user=employee.user
    )  # Access Sale through employee.user
    total_sales = sum(sale.final_price for sale in sales)
    total_transactions = sales.count()
    return total_sales / total_transactions if total_transactions > 0 else 0


def calculate_performance_score(employee):
    """Calculate a performance score for an employee."""
    # Example factors for performance score calculation
    total_sales = calculate_total_sales(employee)
    avg_transaction_value = calculate_average_transaction_value(employee)

    # Normalize and combine metrics (weights are examples; adjust as needed)
    sales_score = min(total_sales / 10000, 1.0) * 50  # Max 50 points
    transaction_score = min(avg_transaction_value / 200, 1.0) * 30  # Max 30 points

    # Combine scores (assuming max score is 100)
    performance_score = sales_score + transaction_score
    return performance_score


@role_required("manager")
def user_activity_report(request):
    activities = UserActivity.objects.all().order_by("-timestamp")

    # Paginate the activities list (10 activities per page)
    paginator = Paginator(activities, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "users/user_activity_report.html", {"page_obj": page_obj})


def log_user_activity(user, action):
    UserActivity.objects.create(user=user, action=action)


def index(request):
    if request.user.is_authenticated:
        return redirect("users:dashboard")
    return render(request, "users/index.html")


@login_required
def profile_view(request):
    return render(request, "users/profile.html")
