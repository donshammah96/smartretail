from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from core.models import Employee as CoreEmployee, Shift
from pos.models import Sale
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum


class CustomUser(AbstractUser):
    """
    Custom user model extending the default AbstractUser.
    Adds additional fields for role, profile picture, address, city, phone number,
    notification preferences, and dashboard customization.
    """
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="employee")
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    notification_preferences = models.TextField(blank=True, null=True)
    dashboard_customization = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="customuser_set", blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"


class Employee(CoreEmployee):
    """
    Employee model extending the core.Employee model.
    Adds a OneToOne relationship with the CustomUser model.
    """
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="employee"
    )

    @property
    def total_sales(self):
        total = self.sales.aggregate(total_sales=Sum("final_price"))["total_sales"]
        return total if total is not None else 0

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class UserActivity(models.Model):
    """
    Model to track user activities.
    Stores the user, action performed, and timestamp of the action.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
    
class TrainingResource(models.Model):
    """
    Model to store training resources.
    Stores the title, description, and file for the resource.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="training_resources/")

    def __str__(self):
        return self.title
    
class Notification(models.Model):
    """
    Model to store notifications.
    Stores the title, message, and timestamp of the notification.
    """
    title = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    