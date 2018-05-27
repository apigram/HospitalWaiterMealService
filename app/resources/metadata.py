from flask_restful import Resource


class RequirementTypeList(Resource):
    def get(self):
        return {
            'requirement_types': {
                'Allergen': 'ALLERGEN',
                'Positive': 'DIETARY_POSITIVE',
                'Negative': 'DIETARY_NEGATIVE'
            }
        }


class MealTimeList(Resource):
    def get(self):
        return {
            'meal_times': {
                'Breakfast': 'BREAKFAST',
                'Lunch': 'LUNCH',
                'Dinner': 'DINNER',
                'Snack': 'SNACK'
            }
        }
