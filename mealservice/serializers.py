from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Meal, Requirement, PatientRequirement, PatientMeal, MealRequirement
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class PatientRequirementSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'patient_pk': 'patient__pk',
    }
    requirement = serializers.HyperlinkedRelatedField(
        view_name='requirement-detail',
        queryset=Requirement.objects.all(),
        many=False,
        read_only=False
    )

    class Meta:
        model = PatientRequirement
        fields = ['url', 'requirement', 'scale']


class MealRequirementSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'meal_pk': 'meal__pk',
    }
    requirement = serializers.HyperlinkedRelatedField(
        view_name='meal-detail',
        queryset=Requirement.objects.all(),
        many=False,
        read_only=False
    )

    class Meta:
        model = MealRequirement
        fields = ['url', 'requirement', 'scale']


class PatientMealSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'patient_pk': 'patient__pk',
    }

    meal = serializers.HyperlinkedRelatedField(
        view_name='meal-detail',
        queryset=Requirement.objects.all(),
        many=False,
        read_only=False
    )

    class Meta:
        model = PatientMeal
        fields = ['url', 'meal', 'quantity']


class RequirementSerializer(serializers.HyperlinkedModelSerializer):
    patients = serializers.HyperlinkedRelatedField(
        view_name='patient-detail',
        many=True,
        read_only=True
    )

    meals = serializers.HyperlinkedRelatedField(
        view_name='meal-detail',
        many=True,
        read_only=True
    )

    class Meta:
        model = Requirement
        fields = ['url', 'label', 'type', 'patients', 'meals']


class MealSerializer(serializers.HyperlinkedModelSerializer):
    requirements = MealRequirementSerializer(many=True, read_only=False)

    patients = serializers.HyperlinkedRelatedField(
        view_name='patient-detail',
        many=True,
        read_only=True
    )

    class Meta:
        model = Meal
        fields = ['url', 'label', 'total_quantity', 'current_quantity', 'time_of_day', 'requirements', 'patients']


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    requirements = PatientRequirementSerializer(many=True, read_only=False)

    meals = serializers.HyperlinkedRelatedField(
        view_name='meal-detail',
        queryset=Meal.objects.all(),
        many=True,
        read_only=False
    )

    class Meta:
        model = Patient
        fields = ['url', 'first_name', 'last_name', 'date_of_birth', 'requirements', 'meals']
