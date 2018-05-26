from flask_restful import Resource, marshal, fields, reqparse
from app import db
from app.models import MealRequirement

# Viewed from requirement details
meal_by_requirement_fields = {
    'label': fields.String,
    'scale': fields.Integer,
    'uri': fields.Url('meal_list_by_requirement'),
    'meal': fields.Url('meal'),
}

# Viewed from meal details
requirement_by_meal_fields = {
    'label': fields.String,
    'scale': fields.Integer,
    'uri': fields.Url('requirement_list_by_meal'),
    'requirement': fields.Url('requirement'),
    'requirement_meal': fields.Url('requirement_meal')
}


class MealListByRequirement(Resource):
    def get(self, id):
        requirement_meals = MealRequirement.query.filter_by(requirement_id=id).all()
        meal_list = [{
            'id': requirement_meal.id,
            'requirement_id': requirement_meal.requirement_id,
            'meal_id': requirement_meal.meal_id,
            'label': requirement_meal.meal.label,
            'scale': requirement_meal.scale
        } for requirement_meal in requirement_meals]

        return {'meals': marshal([meal for meal in meal_list], meal_by_requirement_fields)}


class RequirementListByMeal(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('requirement_id', type=int, required=True,
                                   help='No requirement specified.', location='json')
        self.reqparse.add_argument('scale', type=str, required=True,
                                   help='Scale can only be either Trace or Whole.', location='json')
        super(RequirementListByMeal, self).__init__()

    def get(self, id):
        requirement_meals = MealRequirement.query.filter_by(meal_id=id).all()
        requirement_list = [{
            'id': requirement_meal.id,
            'requirement_id': requirement_meal.requirement_id,
            'meal_id': requirement_meal.meal_id,
            'label': requirement_meal.requirement.label,
            'scale': requirement_meal.scale
        } for requirement_meal in requirement_meals]

        return {'requirements': marshal([meal for meal in requirement_list], requirement_by_meal_fields)}

    def post(self, id):
        args = self.reqparse.parse_args()
        meal = MealRequirement()
        meal.requirement_id = id
        meal.meal_id = args['meal_id']
        meal.scale = args['scale']
        db.session.add(meal)
        db.session.commit()
        return {'requirement': meal.jsonify()}, 201


class MealRequirementResource(Resource):
    def delete(self, meal_id, requirement_id):
        meal_requirement = MealRequirement.query.filter_by(requirement_id=requirement_id, meal_id=meal_id).first()
        db.session.delete(meal_requirement)
        db.session.commit()
        return {'result': True}
