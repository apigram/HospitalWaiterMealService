from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from . import serializers
from .models import Patient, Requirement, Meal, PatientMeal, PatientRequirement, MealRequirement


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = serializers.PatientSerializer


class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = serializers.RequirementSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = serializers.MealSerializer


class PatientRequirementViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return PatientRequirement.objects.filter(patient=self.kwargs['patient_pk'])
    serializer_class = serializers.PatientRequirementSerializer


class MealRequirementViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return MealRequirement.objects.filter(meal=self.kwargs['meal_pk'])
    serializer_class = serializers.MealRequirementSerializer


class PatientMealViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return PatientMeal.objects.filter(patient=self.kwargs['patient_pk'])
    serializer_class = serializers.PatientMealSerializer
