from django.urls import path

from . import views

app_name = 'hrm'

urlpatterns = [
    path("index", views.index, name="index"),
    path("employee_list", views.employee_list, name="employee_list"),
    path("edit_info/<int:id>", views.edit_employee_info,
         name="edit_employee_info"),
]
