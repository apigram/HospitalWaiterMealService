from app import db
from datetime import datetime


class Meal(db.Model):
    __tablename__ = 'meal'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    total_quantity = db.Column(db.Integer)
    current_quantity = db.Column(db.Integer)

    patients = db.relationship('PatientMeal', back_populates='meal')
    requirements = db.relationship('MealRequirement', back_populates='meal')

    def __repr__(self):
        return '<Meal {}>'.format(self.label)

    def set_value(self, column, value):
        if column == 'label':
            self.label = value
        elif column == 'total_quantity':
            self.total_quantity = value
        elif column == 'current_quantity':
            self.current_quantity = value

    def jsonify(self):
        return {
            "id": self.id,
            "label": self.label,
            "total_quantity": self.total_quantity,
            "current_quantity": self.current_quantity
        }


class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)

    requirements = db.relationship('PatientRequirement', back_populates='patient')
    meals = db.relationship('PatientMeal', back_populates='patient')

    def __repr__(self):
        return '<Patient {}>'.format(self.first_name + ' ' + self.last_name)

    def set_value(self, column, value):
        if column == 'first_name':
            self.first_name = value
        elif column == 'last_name':
            self.last_name = value
        elif column == 'date_of_birth':
            self.date_of_birth = datetime.strptime(value, '%d-%m-%Y')

    def jsonify(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": datetime.strftime(self.date_of_birth, '%d-%m-%Y')
        }


class Requirement(db.Model):
    __tablename__ = 'requirement'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    type = db.Column(db.String(20))

    patients = db.relationship('PatientRequirement', back_populates='requirement')
    meals = db.relationship('MealRequirement', back_populates='requirement')

    def __repr__(self):
        return '<Requirement {}>'.format(self.label)

    def set_value(self, column, value):
        if column == 'label':
            self.label = value
        elif column == 'type':
            self.type = value

    def jsonify(self):
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
        }


class PatientMeal(db.Model):
    __tablename__ = 'patient_meal'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    quantity = db.Column(db.Integer)

    patient = db.relationship('Patient', back_populates='meals')
    meal = db.relationship('Meal', back_populates='patients')

    def __repr__(self):
        return '<PatientMeal {}>'.format(self.patient_id + '_' + self.meal_id)

    def set_value(self, column, value):
        if column == 'patient_id':
            self.patient_id = value
        elif column == 'meal_id':
            self.meal_id = value
        elif column == 'quantity':
            self.quantity = value

    def jsonify(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "meal_id": self.meal_id,
            "quantity": self.quantity
        }


class MealRequirement(db.Model):
    __tablename__ = 'meal_requirement'
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirement.id'))
    scale = db.Column(db.String(20))

    meal = db.relationship('Meal', back_populates='requirements')
    requirement = db.relationship('Requirement', back_populates='meals')

    def __repr__(self):
        return '<MealRequirement {}>'.format(self.meal_id + '_' + self.requirement_id)

    def set_value(self, column, value):
        if column == 'meal_id':
            self.meal_id = value
        elif column == 'requirement_id':
            self.requirement_id = value
        elif column == 'scale':
            self.scale = value

    def jsonify(self):
        return {
            "id": self.id,
            "meal_id": self.meal_id,
            "requirement_id": self.requirement_id,
            "scale": self.scale
        }


class PatientRequirement(db.Model):
    __tablename__ = 'patient_requirement'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    requirement_id = db.Column(db.Integer, db.ForeignKey('requirement.id'))
    scale = db.Column(db.String(20))

    patient = db.relationship('Patient', back_populates='requirements')
    requirement = db.relationship('Requirement', back_populates='patients')

    def __repr__(self):
        return '<PatientRequirement {}>'.format(self.patient_id + '_' + self.requirement_id)

    def set_value(self, column, value):
        if column == 'patient_id':
            self.patient_id = value
        elif column == 'requirement_id':
            self.requirement_id = value
        elif column == 'scale':
            self.scale = value

    def jsonify(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "requirement_id": self.requirement_id,
            "scale": self.scale
        }
