from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError, DatabaseError
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
@role_required('employee')
def sales_overview_employee(request):
    sales = Sale.objects.filter(employee=request.user).order_by('-date')
    return render(request, 'users/sales_overview.html', {'sales': sales})

@login_required
@role_required('admin')
def sales_overview_admin(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'users/sales_overview.html', {'sales': sales})

@login_required
@role_required('employee')
def inventory_check_employee(request):
    inventory = Inventory.objects.filter(employee=request.user)
    return render(request, 'core/inventory_check.html', {'inventory': inventory})

@login_required
@role_required('admin')
def inventory_check_admin(request):
    inventory = Inventory.objects.all()
    return render(request, 'core/inventory_check.html', {'inventory': inventory})

@login_required
@role_required('employee')
def training_resources_employee(request):
    resources = TrainingResource.objects.filter(employee=request.user)
    return render(request, 'users/training_resources.html', {'resources': resources})

@login_required
@role_required('admin')
def training_resources_admin(request):
    resources = TrainingResource.objects.all()
    return render(request, 'users/training_resources.html', {'resources': resources})

@login_required
@role_required('employee')
def notifications_employee(request):
    notifications = Notification.objects.filter(employee=request.user).order_by('-date')
    return render(request, 'users/notifications.html', {'notifications': notifications})

@login_required
@role_required('admin')
def notifications_admin(request):
    notifications = Notification.objects.all().order_by('-date')
    return render(request, 'users/notifications.html', {'notifications': notifications})

@login_required
def dashboard(request):
    # Redirect to the appropriate dashboard based on user role
    role_redirects = {
        'admin': 'users:admin_dashboard',
        'manager': 'users:manager_dashboard',
        'employee': 'users:employee_dashboard'
    }
    return redirect(role_redirects.get(request.user.role, 'users:profile'))


@role_required('admin')
def admin_dashboard(request):
    try:
        # Use select_related for related objects
        total_users = CustomUser.objects.count()
        total_employees = CustomUser.objects.filter(role='employee').count()
        total_sales = Sale.objects.select_related('employee').count()

        context = {
            'total_users': total_users,
            'total_employees': total_employees,
            'total_sales': total_sales,
        }
    except DatabaseError as e:
        messages.error(request, "Error retrieving admin data.")
        context = {}

    return render(request, 'users/admin_dashboard.html', context)


@role_required('manager')
def manager_dashboard(request):
    try:
        # Use select_related for optimized query
        total_employees = CustomUser.objects.filter(role='employee').count()
        total_sales = Sale.objects.select_related('employee').filter(employee__role='employee').count()

        context = {
            'total_employees': total_employees,
            'total_sales': total_sales,
        }
    except DatabaseError as e:
        messages.error(request, "Error retrieving manager data.")
        context = {}

    return render(request, 'users/manager_dashboard.html', context)


@role_required('employee')
def employee_dashboard(request):
    try:
        employee = request.user  # Assuming the user is the employee
        context = {
        'employee_name': employee.get_full_name(),  # Assuming the Employee model has a method to get the full name
        'sales_overview_url': reverse('users:sales_overview'),
        'inventory_check_url': reverse('pos:inventory_check'),
        'profile_url': reverse('users:profile'),
        'training_resources_url': reverse('users:training_resources'),
        'notifications_url': reverse('users:notifications'),
        'logout_url': reverse('users:logout'),
    }
    except DatabaseError as e:
        messages.error(request, "Error retrieving employee data.")
        context = {}

    return render(request, 'users/employee_dashboard.html', context)


@role_required(['admin', 'manager'])
def employee_list(request):
    employees = CustomUser.objects.filter(role='employee').select_related('employee_profile')
    return render(request, 'users/employee_list.html', {'employees': employees})


@role_required(['admin', 'manager'])
def employee_profile(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    profile = get_object_or_404(Employee, user=employee)
    return render(request, 'users/employee_profile.html', {'employee': employee, 'profile': profile})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  # This handles session setup
                log_user_activity(user, 'logged in')
                return redirect('users:dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Error processing your login form.")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                log_user_activity(user, 'registered')
                messages.success(request, "Registration successful.")
                return redirect('users:dashboard')
            except IntegrityError:
                messages.error(request, "Error during registration. Please try again.")
        else:
            messages.error(request, "Error processing your registration form.")
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    log_user_activity(request.user, 'logged out')
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('users:login')


@role_required('manager')
def user_performance_report(request):
    employees = Employee.objects.select_related('user')

    for employee in employees:
        employee.total_sales = calculate_total_sales(employee)
        employee.average_transaction_value = calculate_average_transaction_value(employee)
        employee.performance_score = calculate_performance_score(employee)

    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/user_performance_report.html', {'page_obj': page_obj})


@role_required('manager')
def user_activity_report(request):
    activities = UserActivity.objects.all().order_by('-timestamp')

    paginator = Paginator(activities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/user_activity_report.html', {'page_obj': page_obj})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Profile updated successfully.")
            except DatabaseError:
                messages.error(request, "Error updating your profile.")
            return redirect('users:profile')
        else:
            messages.error(request, "Error updating your profile.")
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
            except DatabaseError:
                messages.error(request, "Error changing your password.")
            return redirect('users:profile')
        else:
            messages.error(request, "Error changing your password.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'users/change_password.html', {'form': form})


@role_required('admin')
def delete_profile(request):
    if request.method == 'POST':
        form = UserDeleteForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            try:
                request.user.delete()
                messages.success(request, "Profile deleted successfully.")
                return redirect('users:login')
            except DatabaseError:
                messages.error(request, "Error deleting your profile.")
        else:
            messages.error(request, "Please confirm the deletion.")
    else:
        form = UserDeleteForm()

    return render(request, 'users/delete_profile.html', {'form': form})



@role_required('manager')
def user_performance_report(request):
    employees = Employee.objects.all()  # Get all employees

    # Calculate performance metrics for each employee
    for employee in employees:
        employee.total_sales = calculate_total_sales(employee)
        employee.average_transaction_value = calculate_average_transaction_value(employee)
        employee.performance_score = calculate_performance_score(employee)

    # Paginate the employees list
    paginator = Paginator(employees, 10)  # Show 10 employees per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/user_performance_report.html', {'page_obj': page_obj})


def calculate_total_sales(employee):
    """Calculate the total sales made by an employee."""
    sales = Sale.objects.filter(employee__user=employee.user)  # Access Sale through employee.user
    total_sales = sum(sale.final_price for sale in sales)
    return total_sales


def calculate_average_transaction_value(employee):
    """Calculate the average transaction value for an employee."""
    sales = Sale.objects.filter(employee__user=employee.user)  # Access Sale through employee.user
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


@role_required('manager')
def user_activity_report(request):
    activities = UserActivity.objects.all().order_by('-timestamp')

    # Paginate the activities list (10 activities per page)
    paginator = Paginator(activities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/user_activity_report.html', {'page_obj': page_obj})


def log_user_activity(user, action):
    UserActivity.objects.create(user=user, action=action)


def index(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    return render(request, 'users/index.html')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')
