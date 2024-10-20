from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path("", views.index, name="dashboard"),
    path('<str:model_name>/add/', views.add_view, name='add'),
    path('<str:model_name>/edit/<int:pk>/', views.edit_view, name='edit'),
    path('<str:model_name>/list/', views.generic_list_view, name='list'),
    path('<str:model_name>/detail/<int:pk>/', views.generic_detail_view, name='detail'),
]