from django.conf.urls import url, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'patient', views.PatientViewSet)
router.register(r'requirement', views.RequirementViewSet)
router.register(r'meal', views.MealViewSet)
router.register(r'requirement-type', views.RequirementTypeViewSet)
router.register(r'meal-time', views.MealTimeViewSet)

patient_router = routers.NestedDefaultRouter(router, r'patient', lookup='patient')
patient_router.register(r'requirement', views.PatientRequirementViewSet, base_name='patientrequirement')
patient_router.register(r'meal', views.PatientMealViewSet, base_name='patientmeal')
meal_router = routers.NestedDefaultRouter(router, r'meal', lookup='meal')
meal_router.register(r'requirement', views.MealRequirementViewSet, base_name='mealrequirement')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(patient_router.urls)),
    url(r'^', include(meal_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.CustomAuthToken.as_view())
]
