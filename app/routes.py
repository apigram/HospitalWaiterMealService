from app import app
from flask_restful import Api
from app.resources.meal import MealResource, MealListResource
from app.resources.patient import PatientResource, PatientListResource
from app.resources.requirement import RequirementResource, RequirementListResource
from app.resources.patient_meal import MealListByPatient, PatientListByMeal, PatientMealResource
from app.resources.patient_requirement import PatientListByRequirement, RequirementListByPatient, PatientRequirementResource
from app.resources.meal_requirement import MealListByRequirement, RequirementListByMeal, MealRequirementResource

api = Api(app)

# Simple list/base resources
api.add_resource(MealListResource, '/mealservice/meal',
                 endpoint='meals')
api.add_resource(MealResource, '/mealservice/meal/<int:id>',
                 endpoint='meal')

api.add_resource(PatientListResource, '/mealservice/patient',
                 endpoint='patients')
api.add_resource(PatientResource, '/mealservice/patient/<int:id>',
                 endpoint='patient')

api.add_resource(RequirementListResource, '/mealservice/requirement',
                 endpoint='requirements')
api.add_resource(RequirementResource, '/mealservice/requirement/<int:id>',
                 endpoint='requirement')

# Composite resources
api.add_resource(MealListByPatient, '/mealservice/patient/<int:id>/meal',
                 endpoint='meal_list_by_patient')
api.add_resource(PatientListByMeal, '/mealservice/meal/<int:id>/patient',
                 endpoint='patient_list_by_meal')
api.add_resource(PatientMealResource, '/mealservice/patient/<int:patient_id>/meal/<int:meal_id>',
                 endpoint='patient_meal')

api.add_resource(RequirementListByPatient, '/mealservice/patient/<int:id>/requirement',
                 endpoint='requirement_list_by_patient')
api.add_resource(PatientListByRequirement, '/mealservice/requirement/<int:id>/patient',
                 endpoint='patient_list_by_requirement')
api.add_resource(PatientRequirementResource, '/mealservice/patient/<int:patient_id>/requirement/<int:requirement_id>',
                 endpoint='patient_requirement')

api.add_resource(MealListByRequirement, '/mealservice/requirement/<int:id>/meal',
                 endpoint='meal_list_by_requirement')
api.add_resource(RequirementListByMeal, '/mealservice/meal/<int:id>/requirement',
                 endpoint='requirement_list_by_meal')
api.add_resource(MealRequirementResource, '/mealservice/meal/<int:meal_id>/requirement/<int:requirement_id>',
                 endpoint='meal_requirement')
