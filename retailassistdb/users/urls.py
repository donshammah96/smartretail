from django.urls import include, path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/change_password/", views.change_password, name="change_password"),
    path("profile/delete/", views.delete_profile, name="delete_profile"),
    path("performance-report/", views.user_performance_report, name="user_performance_report"),
    path("activity-report/", views.user_activity_report, name="user_activity_report"),
    # Admin URLs
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    # Manager URLs
    path("manager/dashboard/", views.manager_dashboard, name="manager_dashboard"),
    # URLs for both admin and manager (using include to avoid repetition)
    path(
        "employees/",
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
            ]
        ),
    ),
]