from django.urls import path

import employees.views

urlpatterns = [
    path('create/', employees.views.create_employee, name="create_employee"),
    path('', employees.views.show_all_employees, name="show_employees"),
    path('<employee_id>/update/',
         employees.views.update_employee, name="update_employee"),
    path('<employee_id>/delete/',
         employees.views.delete_employee, name="delete_employee")
]
