import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import login_manager
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Region(SqlAlchemyBase, UserMixin):
    __tablename__ = 'regions'

    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    #эти параметры можно легко высчитать и записать сюда
    members = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    priz = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    pobed = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    def __repr__(self):
        return '<Region %r>' % self.id

    schools = orm.relationship("Schools", back_populates='Region')


