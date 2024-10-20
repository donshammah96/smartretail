from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm, UserEditForm, CustomPasswordChangeForm, UserDeleteForm
from .models import CustomUser, Employee, UserActivity
from pos.models import Sale
from django.core.paginator import Paginator


# Custom decorator for checking user roles (modified to accept a list of roles)
def role_required(roles):
    if not isinstance(roles, list):
        roles = [roles]  # Convert to a list if a single role is provided

    def decorator(view_func):
        @login_required
        @user_passes_test(lambda user: user.role in roles)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return redirect('users:admin_dashboard')
    elif request.user.role == 'manager':
        return redirect('users:manager_dashboard')
    elif request.user.role == 'employee':
        return redirect('users:employee_dashboard')
    else:
        return redirect('users:profile')


@role_required('admin')
def admin_dashboard(request):
    # Get data for the admin dashboard (example)
    total_users = CustomUser.objects.count()
    total_employees = CustomUser.objects.filter(role='employee').count()
    total_sales = Sale.objects.count()

    context = {
        'total_users': total_users,
        'total_employees': total_employees,
        'total_sales': total_sales,
    }
    return render(request, 'users/admin_dashboard.html', context)


@role_required('manager')
def manager_dashboard(request):
    # Example data for manager dashboard
    total_employees = CustomUser.objects.filter(role='employee').count()
    total_sales = Sale.objects.filter(employee__role='employee').count()

    context = {
        'total_employees': total_employees,
        'total_sales': total_sales,
    }
    return render(request, 'users/manager_dashboard.html', context)


@role_required('employee')
def employee_dashboard(request):
    # Example data for employee dashboard
    total_sales = Sale.objects.filter(employee__user=request.user).count()

    context = {
        'total_sales': total_sales,
    }
    return render(request, 'users/employee_dashboard.html', context)


@role_required(['admin', 'manager'])
def employee_list(request):
    employees = CustomUser.objects.filter(role='employee')
    return render(request, 'users/employee_list.html', {'employees': employees})


@role_required(['admin', 'manager'])
def employee_profile(request, pk):
    employee = get_object_or_404(CustomUser, pk=pk)
    profile = get_object_or_404(Employee, user=employee)
    return render(request, 'users/employee_profile.html', {'employee': employee, 'profile': profile})


def login_view(request):
    if request.user.is_authenticated:  # Check if the user is already logged in
        return redirect('users:dashboard')  # Redirect to dashboard if logged in

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                log_user_activity(user, 'logged in')
                return redirect('users:dashboard')  # Redirect to dashboard after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Error processing your login form.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:  # Check if the user is already logged in
        return redirect('users:dashboard')  # Redirect to dashboard if logged in

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Get the user instance
            login(request, user)  # Log in the user after registration
            log_user_activity(user, 'registered')
            messages.success(request, "Registration successful.")
            return redirect('users:dashboard')  # Redirect to dashboard
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


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
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
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Password changed successfully.")
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
            request.user.delete()
            messages.success(request, "Profile deleted successfully.")
            return redirect('users:login')
        else:
            messages.error(request, "Please confirm the deletion.")
    else:
        form = UserDeleteForm()
    return render(request, 'users/delete_profile.html', {'form': form})