import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import login_manager
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Student_point(SqlAlchemyBase, UserMixin):
    __tablename__ = 'students_points'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    student_id = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)
    problem_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


    def __repr__(self):
        return '<Student_point %r>' % self.id


