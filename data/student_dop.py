import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import login_manager
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Person_dop(SqlAlchemyBase, UserMixin):
    __tablename__ = 'students_dop'

    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True, autoincrement=True)
    student_id = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)
    res1 = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)
    res2 = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)
    res3 = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)
    res4 = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)
    num = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)
    date = lastname = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return '<Person_dop %r>' % self.id
