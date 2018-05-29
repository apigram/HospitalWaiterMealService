from flask_restful import Resource, marshal, fields, reqparse
from app import db, auth
from app.models import Requirement

requirement_fields = {
    'label': fields.String,
    'type': fields.String,
    'uri': fields.Url('requirement'),
    'patients': fields.Url('patient_list_by_requirement'),
    'meals': fields.Url('meal_list_by_requirement')
}


class RequirementResource(Resource):
    decorators = [auth.login_required]

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
        return {"result": True, "id": id}


class RequirementListResource(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('label', type=str, location=['json', 'args'])
        self.reqparse.add_argument('type', type=str, location='json')
        super(RequirementListResource, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        if args['label'] is None:
            requirements = Requirement.query.all()
        else:
            requirements = Requirement.query.filter(Requirement.label.contains(args['label'])).all()
        return {'requirements': marshal([requirement for requirement in requirements], requirement_fields)}

    def post(self):
        args = self.reqparse.parse_args()
        requirement = Requirement()
        requirement.label = args['label']
        requirement.type = args['type']
        db.session.add(requirement)
        db.session.commit()
        return {'requirement': marshal(requirement, requirement_fields)}, 201
