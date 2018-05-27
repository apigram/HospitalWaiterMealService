from flask_restful import Resource, marshal, fields, reqparse
from app import db
from app.models import Requirement

requirement_fields = {
    'label': fields.String,
    'type': fields.String,
    'uri': fields.Url('requirement'),
    'patients': fields.Url('patient_list_by_requirement'),
    'meals': fields.Url('meal_list_by_requirement')
}

class RequirementResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, location='json')
        self.reqparse.add_argument('type', type=str, location='json')
        super(RequirementResource, self).__init__()

    def get(self, id):
        requirement = Requirement.query.get_or_404(id)
        return {'requirement': marshal(requirement, requirement_fields)}

    def put(self, id):
        requirement = Requirement.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                requirement.set_value(k, v)
        db.session.commit()
        return {"meal": marshal(requirement, requirement_fields)}

    def delete(self, id):
        requirement = Requirement.query.get_or_404(id)
        db.session.delete(requirement)
        db.session.commit()
        return {"result": True}


class RequirementListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, required=True,
                                   help='No meal label provided.', location='json')
        self.reqparse.add_argument('type', type=str, required=True,
                                   help='Type must be ALLERGEN, DIETARY_POSITIVE or DIETARY_NEGATIVE', location='json')
        super(RequirementListResource, self).__init__()

    def get(self):
        requirements = Requirement.query.all()
        return {'requirements': marshal([requirement for requirement in requirements], requirement_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        requirement = Requirement()
        requirement.label = args['label']
        requirement.type = args['type']
        db.session.add(requirement)
        db.session.commit()
        return {'requirements': requirement.jsonify()}, 201
