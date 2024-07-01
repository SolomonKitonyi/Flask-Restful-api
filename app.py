from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from resources.tm import TMResource, TMListResource, TMStudentsResource
from resources.student import StudentResource, StudentListResource, StudentTMResource

# TM Routes
api.add_resource(TMListResource, '/tms')
api.add_resource(TMResource, '/tms/<int:id>')
api.add_resource(TMStudentsResource, '/tms/<int:id>/students')

# Student Routes
api.add_resource(StudentListResource, '/students')
api.add_resource(StudentResource, '/students/<int:id>')
api.add_resource(StudentTMResource, '/students/<int:id>/tm')

if __name__ == '__main__':
    app.run(debug=True)
