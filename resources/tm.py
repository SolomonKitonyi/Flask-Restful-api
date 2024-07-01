from flask_restful import Resource, reqparse
from models import TM, Student
from app import db

tm_parser = reqparse.RequestParser()
tm_parser.add_argument('first_name', type=str, required=True, help='First name is required')
tm_parser.add_argument('last_name', type=str, required=True, help='Last name is required')

class TMResource(Resource):
    def get(self, id):
        tm = TM.query.get(id)
        if not tm:
            return {'message': 'TM not found'}, 404
        return {'id': tm.id, 'first_name': tm.first_name, 'last_name': tm.last_name}

    def put(self, id):
        data = tm_parser.parse_args()
        tm = TM.query.get(id)
        if not tm:
            return {'message': 'TM not found'}, 404
        tm.first_name = data['first_name']
        tm.last_name = data['last_name']
        db.session.commit()
        return {'message': 'TM updated successfully'}

    def delete(self, id):
        tm = TM.query.get(id)
        if not tm:
            return {'message': 'TM not found'}, 404
        db.session.delete(tm)
        db.session.commit()
        return {'message': 'TM deleted successfully'}

class TMListResource(Resource):
    def get(self):
        tms = TM.query.all()
        return [{'id': tm.id, 'first_name': tm.first_name, 'last_name': tm.last_name} for tm in tms]

    def post(self):
        data = tm_parser.parse_args()
        new_tm = TM(first_name=data['first_name'], last_name=data['last_name'])
        db.session.add(new_tm)
        db.session.commit()
        return {'message': 'TM created successfully'}, 201

class TMStudentsResource(Resource):
    def get(self, id):
        tm = TM.query.get(id)
        if not tm:
            return {'message': 'TM not found'}, 404
        students = Student.query.filter_by(tm_id=id).all()
        return [{'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name, 'course': student.course} for student in students]
