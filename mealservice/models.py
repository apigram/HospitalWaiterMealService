from django.db import models
from django.contrib.auth.models import User


class MealTime(models.Model):
    label = models.CharField(max_length=20)


class RequirementType(models.Model):
    COLOURS = [
        ('red', 'red'),
        ('yellow', 'yellow'),
        ('green', 'green')
    ]
    label = models.CharField(max_length=20)
    colour = models.CharField(max_length=10, choices=COLOURS)


# Create your models here.
class Requirement(models.Model):
    label = models.CharField(max_length=100)
    type = models.ForeignKey(RequirementType, on_delete=models.CASCADE)


class Meal(models.Model):
    label = models.CharField(max_length=100)
    total_quantity = models.IntegerField(default=0)
    current_quantity = models.IntegerField(default=0)
    time_of_day = models.ForeignKey(MealTime, on_delete=models.CASCADE)

    meal_requirements = models.ManyToManyField(Requirement, through='MealRequirement', related_name='meal')


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Date of Birth')

    patient_requirements = models.ManyToManyField(Requirement, through='PatientRequirement', related_name='patient')
    patient_meals = models.ManyToManyField(Meal, through='PatientMeal', related_name='patient')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')


class PatientRequirement(models.Model):
    SCALE_LIST = [
        ('WHOLE', 'Whole'),
        ('TRACE', 'Trace')
    ]
    scale = models.CharField(max_length=20, choices=SCALE_LIST)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='requirements')
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='patients')


class PatientMeal(models.Model):
    quantity = models.IntegerField()

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='meals')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='patients')


class MealRequirement(models.Model):
    SCALE_LIST = [
        ('WHOLE', 'Whole'),
        ('TRACE', 'Trace')
    ]
    scale = models.CharField(max_length=20, choices=SCALE_LIST)

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='requirements')
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='meals')
