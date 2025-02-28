import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import login_manager
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Person(SqlAlchemyBase, UserMixin):
    __tablename__ = 'people'

    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True, autoincrement=True)
    firstname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    lastname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    score = sqlalchemy.Column(sqlalchemy.Integer)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    #id школы
    school = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    role = sqlalchemy.Column(sqlalchemy.Integer,nullable=False)

    def __repr__(self):
        return '<Person %r>' % self.id


