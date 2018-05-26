from flask_restful import Resource, marshal, fields, reqparse
from app import db
from app.models import PatientRequirement

# Viewed from patient details
requirement_by_patient_fields = {
    'label': fields.String,
    'scale': fields.String,
    'uri': fields.Url('requirement_list_by_patient'),
    'requirement': fields.Url('requirement'),
    'patient_requirement': fields.Url('patient_requirement')
}

# Viewed from requirement details
patient_by_requirement_fields = {
    'patient_name': fields.String,
    'scale': fields.String,
    'uri': fields.Url('patient_list_by_requirement'),
    'patient': fields.Url('patient'),
    'patient_requirement': fields.Url('patient_requirement')
}


class RequirementListByPatient(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('requirement_id', type=int, required=True,
                                   help='No total quantity provided.', location='json')
        self.reqparse.add_argument('scale', type=str, required=True,
                                   help='Scale must be either Trace or Whole', location='json')
        super(RequirementListByPatient, self).__init__()

    def get(self, id):
        patient_requirements = PatientRequirement.query.filter_by(patient_id=id).all()
        requirement_list = [{
            'id': patient_requirement.id,
            'patient_id': patient_requirement.patient_id,
            'requirement_id': patient_requirement.requirement_id,
            'label': patient_requirement.requirement.label,
            'scale': patient_requirement.scale
        } for patient_requirement in patient_requirements]

        return {'requirements': marshal([requirement for requirement in requirement_list], requirement_by_patient_fields)}

    def post(self, id):
        args = self.reqparse.parse_args()
        requirement = PatientRequirement()
        requirement.patient_id = id
        requirement.requirement_id = args['requirement_id']
        requirement.scale = args['scale']
        db.session.add(requirement)
        db.session.commit()
        return {'requirement': requirement.jsonify()}, 201


class PatientListByRequirement(Resource):
    def get(self, id):
        patient_requirements = PatientRequirement.query.filter_by(requirement_id=id).all()
        patient_list = [{
            'id': patient_requirement.id,
            'patient_id': patient_requirement.patient_id,
            'requirement_id': patient_requirement.requirement_id,
            'patient_name': patient_requirement.patient.first_name + ' ' + patient_requirement.patient.last_name,
            'scale': patient_requirement.scale
        } for patient_requirement in patient_requirements]

        return {'patients': marshal([requirement for requirement in patient_list], patient_by_requirement_fields)}


class PatientRequirementResource(Resource):
    def delete(self, patient_id, requirement_id):
        patient_requirement = PatientRequirement.query.filter_by(patient_id=patient_id, requirement_id=requirement_id).first()
        db.session.delete(patient_requirement)
        db.session.commit()
        return {'result': True}
