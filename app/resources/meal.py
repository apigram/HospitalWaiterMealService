from flask_restful import Resource, marshal, fields, reqparse
from app import db
from app.models import Meal

meal_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'total_quantity': fields.Integer,
    'current_quantity': fields.Integer,
    'time_of_day': fields.String,
    'uri': fields.Url('meal'),
    'patients': fields.Url('patient_list_by_meal'),
    'patient_meal': fields.Url('meal_list_by_patient'),
    'requirements': fields.Url('requirement_list_by_meal')
}


class MealResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, location='json')
        self.reqparse.add_argument('total_quantity', type=str, location='json')
        self.reqparse.add_argument('current_quantity', type=str, location='json')
        super(MealResource, self).__init__()

    def get(self, id):
        meal = Meal.query.get_or_404(id)
        return {'meal': marshal(meal, meal_fields)}

    def put(self, id):
        meal = Meal.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                meal.set_value(k, v)
        db.session.commit()
        return {"meal": marshal(meal, meal_fields)}

    def delete(self, id):
        meal = Meal.query.get_or_404(id)
        db.session.delete(meal)
        db.session.commit()
        return {"result": True}


class MealListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, required=True,
                                   help='No meal label provided.', location='json')
        self.reqparse.add_argument('total_quantity', type=int, required=True,
                                   help='No total quantity provided.', location='json')
        self.reqparse.add_argument('time_of_day', type=str, required=True,
                                   help='Must be either Breakfast, Lunch or Dinner', location='json')
        super(MealListResource, self).__init__()

    def get(self):
        meals = Meal.query.all()
        return {'meals': marshal([meal for meal in meals], meal_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        meal = Meal()
        meal.label = args['label']
        meal.total_quantity = args['total_quantity']
        meal.current_quantity = args['total_quantity']
        meal.time_of_day = args['time_of_day']
        db.session.add(meal)
        db.session.commit()
        return {'meal': meal.jsonify()}, 201
