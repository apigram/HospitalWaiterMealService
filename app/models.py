from app import db


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    total_quantity = db.Column(db.Integer)
    current_quantity = db.Column(db.Integer)

    def __repr__(self):
        return '<Meal {}>'.format(self.label)

    def jsonify(self):
        return {
            "id": self.id,
            "label": self.label,
            "total_quantity": self.total_quantity,
            "current_quantity": self.current_quantity
        }


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)

    def __repr__(self):
        return '<Patient {}>'.format(self.first_name + ' ' + self.last_name)

    def jsonify(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth
        }


class Requirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    type = db.Column(db.String(20))

    def __repr__(self):
        return '<Requirement {}>'.format(self.label)

    def jsonify(self):
        return {
            "id": self.id,
            "label": self.label,
            "type": self.total_quantity,
        }
