from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import EmployeeForm
from .models import Employee


# Create your views here.
def show_all_employees(request):
    all_employees = Employee.objects.all()
    return render(request, 'employees/show_all_employees.template.html', {
        'all_employees': all_employees
    })


def create_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('show_employees'))
        else:
            return render(request, 'employees/create_employee.template.html', {
                "form": form
            })
    else:
        form = EmployeeForm()
        return render(request, 'employees/create_employee.template.html', {
            "form": form
        })


def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect(reverse('show_employees'))
        else:
            return render(request, 'employees/update_employee.template.html', {
                'form': form
            })
    else:

        form = EmployeeForm(instance=employee)
        return render(request, 'employees/update_employee.template.html', {
            'form': form
        })


def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        employee.delete()
        return redirect(reverse('show_employees'))
    else:
        return render(request,
                      'employees/confirm_to_delete_employee.template.html', {
                       'employee': employee
                      })
