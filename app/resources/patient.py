from flask_restful import Resource, marshal, fields, reqparse
from app import db
from app.models import Patient
import datetime

patient_fields = {
    'first_name': fields.String,
    'last_name': fields.String,
    'date_of_birth': fields.String,
    'uri': fields.Url('patient'),
    'requirements': fields.Url('requirement_list_by_patient'),
    'meals': fields.Url('meal_list_by_patient')
}


class PatientResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, location='json')
        self.reqparse.add_argument('last_name', type=str, location='json')
        self.reqparse.add_argument('date_of_birth', type=str, location='json')
        super(PatientResource, self).__init__()

    def get(self, id):
        patient = Patient.query.get_or_404(id)
        return {'patient': marshal(patient, patient_fields)}

    def put(self, id):
        patient = Patient.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                patient.set_value(k, v)
        db.session.commit()
        return {"patient": marshal(patient, patient_fields)}

    def delete(self, id):
        patient = Patient.query.get_or_404(id)
        db.session.delete(patient)
        db.session.commit()
        return {"result": True}


class PatientListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=True,
                                   help='No first name provided.', location='json')
        self.reqparse.add_argument('last_name', type=str, required=True,
                                   help='No last name provided.', location='json')
        self.reqparse.add_argument('date_of_birth', type=str, required=True,
                                   help='No date of birth provided.', location='json')
        super(PatientListResource, self).__init__()

    def get(self):
        patients = Patient.query.all()
        return {'patients': marshal([patient for patient in patients], patient_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        patient = Patient()
        patient.first_name = args['first_name']
        patient.last_name = args['last_name']
        patient.date_of_birth = datetime.datetime.strptime(args['date_of_birth'], '%d-%m-%Y')
        db.session.add(patient)
        db.session.commit()
        return {'patient': patient.jsonify()}, 201
