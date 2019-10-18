from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Meal, Requirement, PatientRequirement, PatientMeal, MealRequirement, RequirementType, MealTime
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer


class RequirementTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RequirementType
        fields = ['url', 'label', 'colour']


class MealTimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MealTime
        fields = ['url', 'label']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    patient = serializers.HyperlinkedRelatedField(
        view_name='patient-detail',
        many=False,
        read_only=True
    )

    class Meta:
        model = User
        fields = ['url', 'username', 'patient', 'email', 'is_staff']


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
        view_name='requirement-detail',
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

    patient = serializers.HyperlinkedRelatedField(
        view_name='patient-detail',
        queryset=Patient.objects.all(),
        many=False,
        read_only=False
    )

    meal = serializers.HyperlinkedRelatedField(
        view_name='meal-detail',
        queryset=Meal.objects.all(),
        many=False,
        read_only=False
    )

    class Meta:
        model = PatientMeal
        fields = ['url', 'patient', 'meal', 'quantity']


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

    type = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=RequirementType.objects.all(),
        slug_field='label'
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

    time_of_day = serializers.SlugRelatedField(
        queryset=MealTime.objects.all(),
        many=False,
        read_only=False,
        slug_field='label'
    )

    def create(self, validated_data):
        requirement_list_data = validated_data.pop('requirements')
        meal = Meal.objects.create(**validated_data)
        for requirement_data in requirement_list_data:
            requirement = requirement_data.pop('requirement')
            scale = requirement_data.pop('scale')
            MealRequirement.objects.create(meal=meal, requirement=requirement, scale=scale)

        return meal

    class Meta:
        model = Meal
        fields = ['url', 'label', 'total_quantity', 'current_quantity', 'time_of_day', 'requirements', 'patients']


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    requirements = PatientRequirementSerializer(many=True, read_only=False)

    meals = PatientMealSerializer(many=True, read_only=True)

    def create(self, validated_data):
        requirement_list_data = validated_data.pop('requirements')
        patient = Patient.objects.create(**validated_data)
        for requirement_data in requirement_list_data:
            requirement = requirement_data.pop('requirement')
            scale = requirement_data.pop('scale')
            PatientRequirement.objects.create(patient=patient, requirement=requirement, scale=scale)
        return patient

    class Meta:
        model = Patient
        fields = ['url', 'first_name', 'last_name', 'date_of_birth', 'requirements', 'meals']
