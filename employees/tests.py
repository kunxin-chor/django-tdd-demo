from .forms import EmployeeForm
from .models import Employee, Department, MedicalLeave
from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from faker import Faker

fake = Faker()


# Create your tests here.


class EmployeeModelTestCase(TestCase):

    def test_employee_has_default_14_days_leave(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        # 2. create the Employee model instance
        employee = Employee()
        employee.employee_number = 441512
        employee.first_name = "Ah Kow"
        employee.last_name = "Tan"
        employee.salary = 1200
        employee.months_employed = 3
        employee.user = user
        employee.department = department
        employee.save()

        # 3. test that save has been done correctly
        # if done correct, an id will be assigned to the employee object
        self.assertTrue(employee.id > 0)

        # 4. retrieve the employee from the database
        test_employee = get_object_or_404(Employee, pk=employee.id)

        # 5. test if the employee's default number of leave is 14
        self.assertEqual(test_employee.leave, 14)

        self.assertEqual(test_employee.get_remaining_leave(), 14)


class EmployeeFormTestCase(TestCase):

    def test_validate_if_employee_number_less_than_6_digits(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        # 2. create the form
        form = EmployeeForm({
            "employee_number": 1234,
            "first_name": "Ah Kow",
            "last_name": "Tan",
            "salary": 2000,
            "months_employed": 3,
            "user": user,
            "department": department,
            "leave": 14
        })
        self.assertFalse(form.is_valid())

    def test_validate_if_employee_number_more_than_6_digits(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        # 2. create the form
        form = EmployeeForm({
            "employee_number": 12345678,
            "first_name": "Ah Kow",
            "last_name": "Tan",
            "salary": 2000,
            "months_employed": 3,
            "user": user,
            "department": department,
            "leave": 14
        })
        self.assertFalse(form.is_valid())

    def test_validate_if_employee_number_is_valid(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        # 2. create the form
        form = EmployeeForm({
            "employee_number": 123456,
            "first_name": "Ah Kow",
            "last_name": "Tan",
            "salary": 2000,
            "months_employed": 3,
            "user": user,
            "department": department,
            "leave": 14
        })
        self.assertTrue(form.is_valid())


class EmployeeRoutesTestCase(TestCase):

    def test_can_get_create_employee_form(self):
        response = self.client.get('/employees/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('employees/create_template.html')

    def test_can_post_create_employee(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        raw_data = {
            "employee_number": 123456,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "salary": 2000,
            "months_employed": 3,
            "user": str(user.id),
            "department": str(department.id),
            "leave": 14
        }

        response = self.client.post('/employees/create/', raw_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_employees'))

        # find employee with first name and last name combo
        new_employee = Employee.objects.get(
            first_name=raw_data["first_name"], last_name=raw_data["last_name"])

        # assert that the new employee has been added correctly
        self.assertNotEqual(new_employee, None)

        # assert that the provided data has been added correctly
        self.assertEqual(new_employee.first_name, raw_data["first_name"])
        self.assertEqual(new_employee.last_name, raw_data["last_name"])
        self.assertEqual(str(new_employee.department.id),
                         raw_data["department"])
        self.assertEqual(new_employee.leave, raw_data["leave"])
        self.assertEqual(str(new_employee.user.id), raw_data["user"])
        self.assertEqual(new_employee.salary, raw_data["salary"])
        self.assertEqual(new_employee.months_employed,
                         raw_data["months_employed"])

    def test_can_show_edit_employee_form(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        raw_data = {
            "employee_number": 412413,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "salary": 3333,
            "months_employed": 1314,
            "user": user,
            "department": department,
            "leave": 2314
        }

        # pass dictionary as named parameters to a function call
        employee = Employee(**raw_data)
        employee.save()

        # 2. display the edit form
        response = self.client.get(f'/employees/{employee.id}/update/')

        # 3. assert route is rendered correctly and with the correcte template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'employees/update_employee.template.html')

        # 4. assert that each of the individual fields are in the form
        for key, data in raw_data.items():
            self.assertContains(response, str(data))

    def test_update_employee(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        raw_data = {
            "employee_number": 412413,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "salary": 3333,
            "months_employed": 1314,
            "user": user,
            "department": department,
            "leave": 2314
        }

        # pass dictionary as named parameters to a function call
        employee = Employee(**raw_data)
        employee.save()

        # 2. create the data that we want to change to

        user2 = User.objects.create_user(username="John Doe")
        department2 = Department.objects.create(name="Human Resources")

        modified_data = {
            "employee_number": 514512,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "salary": 33334,
            "months_employed": 13144,
            "user": str(user2.id),
            "department": str(department2.id),
            "leave": 2315
        }

        # 3. send the response and make sure page is redirected
        response = self.client.post(
            f'/employees/{employee.id}/update/', modified_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_employees'))

        # 4. retrieve the employee from database and see if it has been updated
        modified_employee = get_object_or_404(Employee, pk=employee.id)

        modified_data["user"] = user2
        modified_data["department"] = department2

        for key, data in modified_data.items():
            self.assertEquals(getattr(modified_employee, key), data)

    def test_delete_employee(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        raw_data = {
            "employee_number": 412413,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "salary": 3333,
            "months_employed": 1314,
            "user": user,
            "department": department,
            "leave": 2314
        }

        # pass dictionary as named parameters to a function call
        employee = Employee(**raw_data)
        employee.save()

        # 2. get the form
        response = self.client.get(f'/employees/{employee.id}/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "employees/confirm_to_delete_employee.template.html")
        self.assertContains(response, employee.first_name)
        self.assertContains(response, employee.last_name)

    def test_actual_delete_employee(self):
        # 1. create the model instances required for the relationships
        user = User.objects.create_user(username="Ah Kow")
        department = Department.objects.create(name="Accounting")

        raw_data = {
            "employee_number": 412413,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "salary": 3333,
            "months_employed": 1314,
            "user": user,
            "department": department,
            "leave": 2314
        }

        # pass dictionary as named parameters to a function call
        employee = Employee(**raw_data)
        employee.save()

        # 2. perform the delete
        response = self.client.post(f'/employees/{employee.id}/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_employees'))

        # 3. check if the employee still exists. It shouldn't
        deleted_employee = Employee.objects.filter(pk=employee.id).first()
        self.assertEquals(deleted_employee, None)
