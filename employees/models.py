from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    employee_number = models.PositiveIntegerField(blank=False, unique=True)
    first_name = models.CharField(blank=False, max_length=255)
    last_name = models.CharField(blank=False, max_length=255)
    salary = models.PositiveIntegerField(blank=False)
    months_employed = models.PositiveSmallIntegerField(blank=False)
    leave = models.PositiveSmallIntegerField(blank=False, default=14)
    department = models.ForeignKey('Department', on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.employee_number} - {self.first_name} {self.last_name}"

    def get_remaining_leave(self):
        return self.leave - self.medicalleave_set.count()


class Department(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name


class MedicalLeave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)

    def __str__(self):
        return f"Medicial leave ({self.start_date} to {self.end_date}) for " \
               f"{self.employee.first_name}"

    def get_days(self):
        return abs((self.start_end_date - self.start_date).days)


class Team(models.Model):
    name = models.CharField(blank=False, max_length=255)
    members = models.ManyToManyField(Employee, through="Membership")

    def __str__(self):
        return self.name


class Membership(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now=True)
    role = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return f"Membership {self.id}"
