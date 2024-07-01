from flask_restful import Resource, reqparse
from models import Student, TM
from app import db

student_parser = reqparse.RequestParser()
student_parser.add_argument('first_name', type=str, required=True, help='First name is required')
student_parser.add_argument('last_name', type=str, required=True, help='Last name is required')
student_parser.add_argument('course', type=str, required=True, help='Course is required')
student_parser.add_argument('tm_id', type=int, required=True, help='TM ID is required')

class StudentResource(Resource):
    def get(self, id):
        student = Student.query.get(id)
        if not student:
            return {'message': 'Student not found'}, 404
        return {'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name, 'course': student.course, 'tm_id': student.tm_id}

    def put(self, id):
        data = student_parser.parse_args()
        student = Student.query.get(id)
        if not student:
            return {'message': 'Student not found'}, 404
        student.first_name = data['first_name']
        student.last_name = data['last_name']
        student.course = data['course']
        student.tm_id = data['tm_id']
        db.session.commit()
        return {'message': 'Student updated successfully'}

    def delete(self, id):
        student = Student.query.get(id)
        if not student:
            return {'message': 'Student not found'}, 404
        db.session.delete(student)
        db.session.commit()
        return {'message': 'Student deleted successfully'}

class StudentListResource(Resource):
    def get(self):
        students = Student.query.all()
        return [{'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name, 'course': student.course, 'tm_id': student.tm_id} for student in students]

    def post(self):
        data = student_parser.parse_args()
        new_student = Student(first_name=data['first_name'], last_name=data['last_name'], course=data['course'], tm_id=data['tm_id'])
        db.session.add(new_student)
        db.session.commit()
        return {'message': 'Student created successfully'}, 201

class StudentTMResource(Resource):
    def get(self, id):
        student = Student.query.get(id)
        if not student:
            return {'message': 'Student not found'}, 404
        tm = TM.query.get(student.tm_id)
        return {'id': tm.id, 'first_name': tm.first_name, 'last_name': tm.last_name}
