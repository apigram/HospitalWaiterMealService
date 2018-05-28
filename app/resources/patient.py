from flask_restful import Resource, marshal, fields, reqparse
from app import app, db, mail
from app.models import Patient, User
import datetime
import random
from flask_mail import Message
import bcrypt

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
        self.reqparse.add_argument('first_name', type=str, location='json')
        self.reqparse.add_argument('last_name', type=str, location='json')
        self.reqparse.add_argument('name', type=str, location='args')
        self.reqparse.add_argument('date_of_birth', type=str, location='json')
        self.reqparse.add_argument('email', type=str, location='json')
        super(PatientListResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        if args['name'] is None:
            patients = Patient.query.all()
        else:
            patients = Patient.query.filter(Patient.first_name.contains(args['name'])).all()

        return {'patients': marshal([patient for patient in patients], patient_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        patient = Patient()
        patient.first_name = args['first_name']
        patient.last_name = args['last_name']
        patient.date_of_birth = datetime.datetime.strptime(args['date_of_birth'], '%Y-%m-%d')
        user = User()
        user.username = patient.first_name[0].lower() + patient.last_name.lower()
        user.email = args['email']
        password = "%09d" % (random.randrange(1, 9999999999),)
        msg = Message(subject="Password",
                      recipients=[user.email],
                      body="Your credentials to log into the HospitalWaiter application is as follows:\n\n"
                           "Username: %s\n"
                           "Password: %s\n\n"
                           "Keep these credentials secure!" % (user.username, password))
        with app.app_context():
            mail.send(msg)

        user.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10))

        db.session.add(patient)
        db.session.commit()

        user.patient_id = patient.id
        db.session.add(user)
        db.session.commit()
        return {'patient': marshal(patient, patient_fields)}, 201
