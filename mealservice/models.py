from django.db import models


# Create your models here.
class Requirement(models.Model):
    REQUIREMENT_TYPES = [
        ('ALLERGEN', 'Allergy'),
        ('DIETARY_POSITIVE', 'Positive'),
        ('DIETARY_NEGATIVE', 'Negative'),
    ]

    label = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=REQUIREMENT_TYPES)


class Meal(models.Model):
    MEAL_TIMES = [
        ('BREAKFAST', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
        ('SNACK', 'Snack'),
    ]
    label = models.CharField(max_length=100)
    total_quantity = models.IntegerField(default=0)
    current_quantity = models.IntegerField(default=0)
    time_of_day = models.CharField(max_length=20, choices=MEAL_TIMES)

    meal_requirements = models.ManyToManyField(Requirement, through='MealRequirement', related_name='meal')


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Date of Birth')

    patient_requirements = models.ManyToManyField(Requirement, through='PatientRequirement', related_name='patient')
    patient_meals = models.ManyToManyField(Meal, through='PatientMeal', related_name='patient')


class PatientRequirement(models.Model):
    scale = models.CharField(max_length=20)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='requirements')
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='patients')


class PatientMeal(models.Model):
    quantity = models.IntegerField()

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='meals')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='patients')


class MealRequirement(models.Model):
    scale = models.CharField(max_length=20)

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='requirements')
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, related_name='meals')
