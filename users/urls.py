from django.urls import path, include
from . import views
from .views import ManagerDashboardView, AdminDashboardView, EmployeeDashboardView

app_name = "users"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/change_password/", views.change_password, name="change_password"),
    path("profile/delete/", views.delete_profile, name="delete_profile"),
    path("user_performance_report/", views.user_performance_report, name="user_performance_report"),
    # Dashboard URLs
     path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/admin/", AdminDashboardView.as_view(), name="manager_dashboard"),
    path("dashboard/manager/", ManagerDashboardView.as_view(), name="manager_dashboard"),
    path("dashboard/employee/", EmployeeDashboardView.as_view(), name="employee_dashboard"),
    # URLs for both admin and manager
    path(
        "employee/",
        include(
            [
                path("", views.employee_list, name="employee_list"),
                path("<int:pk>/", views.employee_profile, name="employee_profile"),
                path(
                    "performance-report/",
                    views.user_performance_report,
                    name="user_performance_report",
                ),
                path(
                    "activity-report/",
                    views.user_activity_report,
                    name="user_activity_report",
                ),
                # ... other employee-related URLs ...
            ]
        ),
    ),
    # Other URLs (sales overview, inventory check, etc.)
    path("sales-overview/", views.sales_overview_employee, name="sales_overview"),
    path("inventory-check/", views.inventory_check_employee, name="inventory_check"),
    # ...
]
