from django import forms
from django.core.exceptions import ValidationError

from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

    def clean_employee_number(self):
        data = self.cleaned_data["employee_number"]

        # check if employee number is 6 digits
        if data < 100000 or data > 999999:
            raise ValidationError("Employee number must be 6 digits")
        return data
