from flask_restful import Api
from app import app
from app import resources
from flask_restful import Api

api = Api(app)
api.add_resource(resources.MealListResource, '/mealservice/meal', endpoint='meals')
api.add_resource(resources.MealResource, '/mealservice/meal/<int:id>', endpoint='meal')
api.add_resource(resources.PatientListResource, '/mealservice/patient', endpoint='patients')
api.add_resource(resources.PatientResource, '/mealservice/patient/<int:id>', endpoint='patient')
api.add_resource(resources.RequirementListResource, '/mealservice/requirement', endpoint='requirements')
api.add_resource(resources.RequirementResource, '/mealservice/requirement/<int:id>', endpoint='requirement')
