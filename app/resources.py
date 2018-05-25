from flask_restful import Resource, marshal, fields, reqparse
from flask import abort
from app import db
from app import models
import datetime

meal_fields = {
    'label': fields.String,
    'total_quantity': fields.Integer,
    'current_quantity': fields.Integer,
    'uri': fields.Url('meal')
}

patient_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'date_of_birth': fields.String,
    'uri': fields.Url('patient')
}

requirement_fields = {
    'label': fields.String,
    'type': fields.String,
    'uri': fields.Url('requirement')
}


class MealResource(Resource):
    def __init__(self):
        super(MealResource, self).__init__()

    def get(self, id):
        meal = models.Meal.query.get(id)
        if meal is None:
            abort(404)
        return {'meal': marshal(meal, meal_fields)}

    def put(self, id):
        pass

    def delete(self, id):
        meal = models.Meal.query.get(id)
        if meal is None:
            abort(500)
        db.session.delete()
        return {"result": True}


class MealListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, required=True,
                                   help='No meal label provided.', location='json')
        self.reqparse.add_argument('total_quantity', type=int, required=True,
                                   help='No total quantity provided.', location='json')
        super(MealListResource, self).__init__()

    def get(self):
        meals = models.Meal.query.all()
        return {'meals': marshal([meal for meal in meals], meal_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        meal = models.Meal()
        meal.label = args['label']
        meal.total_quantity = args['total_quantity']
        meal.current_quantity = args['total_quantity']
        db.session.add(meal)
        db.session.commit()
        return {'meal': meal.jsonify()}, 201


class PatientResource(Resource):
    def __init__(self):
        super(PatientResource, self).__init__()

    def get(self, id):
        patient = models.Patient.query.get(id)
        if patient is None:
            abort(404)
        return {'patient': marshal(patient, patient_fields)}

    def put(self, id):
        pass

    def delete(self, id):
        patient = models.Patient.query.get(id)
        if patient is None:
            abort(500)
        db.session.delete()
        return {"result": True}


class PatientListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=True,
                                   help='No first name provided.', location='json')
        self.reqparse.add_argument('first_name', type=str, required=True,
                                   help='No last name provided.', location='json')
        self.reqparse.add_argument('date_of_birth', type=str, required=True,
                                   help='No date of birth provided.', location='json')
        super(PatientListResource, self).__init__()

    def get(self):
        patients = models.Patient.query.all()
        return {'patients': marshal([patient for  patient in patients], patient_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        patient = models.Patient()
        patient.first_name = args['first_name']
        patient.last_name = args['last_name']
        patient.date_of_birth = datetime.datetime.strptime(args['date_of_birth'], '%d-%m-%y')
        db.session.add(patient)
        db.session.commit()
        return {'patient': patient.jsonify()}, 201


class RequirementResource(Resource):
    def __init__(self):
        super(RequirementResource, self).__init__()

    def get(self, id):
        requirement = models.Requirement.query.get(id)
        if requirement is None:
            abort(404)
        return {'requirement': marshal(requirement, requirement_fields)}

    def put(self, id):
        pass

    def delete(self, id):
        requirement = models.Requirement.query.get(id)
        if requirement is None:
            abort(500)
        db.session.delete()
        return {"result": True}


class RequirementListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, required=True,
                                   help='No meal label provided.', location='json')
        self.reqparse.add_argument('total_quantity', type=int, required=True,
                                   help='No total quantity provided.', location='json')
        super(RequirementListResource, self).__init__()

    def get(self):
        meals = models.Meal.query.all()
        return {'requirements': marshal([meal for meal in meals], meal_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        requirement = models.Requirement()
        requirement.label = args['label']
        requirement.type = args['type']
        db.session.add(requirement)
        db.session.commit()
        return {'requirements': requirement.jsonify()}, 201
