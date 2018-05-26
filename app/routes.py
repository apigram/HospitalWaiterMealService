from app import app
from flask_restful import Api
from app.resources.meal import MealResource, MealListResource
from app.resources.patient import PatientResource, PatientListResource
from app.resources.requirement import RequirementResource, RequirementListResource

api = Api(app)
api.add_resource(MealListResource, '/mealservice/meal', endpoint='meals')
api.add_resource(MealResource, '/mealservice/meal/<int:id>', endpoint='meal')
api.add_resource(PatientListResource, '/mealservice/patient', endpoint='patients')
api.add_resource(PatientResource, '/mealservice/patient/<int:id>', endpoint='patient')
api.add_resource(RequirementListResource, '/mealservice/requirement', endpoint='requirements')
api.add_resource(RequirementResource, '/mealservice/requirement/<int:id>', endpoint='requirement')
