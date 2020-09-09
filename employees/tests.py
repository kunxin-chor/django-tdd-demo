from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Employee, Department, MedicalLeave

# Create your tests here.


class EmployeeModelTestCase(TestCase):

    def test_employee_has_default_14_days_leave(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create_department(name="Accounting")

        # 2. create the Employee model instance
        employee = Employee()
        employee.first_name = "Ah Kow"
        employee.last_name = "Tan"
        employee.salary = 1200
        employee.months_employed = 3
        employee.user = user
        employee.owner = department
        employee.save()

        # 3. test that save has been done correctly
        # if done correct, an id will be assigned to the employee object
        self.assertTrue(employee.id > 0)

        # 4. retrieve the employee from the database
        test_employee = get_object_or_404(Employee, employee.id)

        # 5. test if the employee's default number of leave is 14
        self.assertEqual(test_employee.leave, 14)
