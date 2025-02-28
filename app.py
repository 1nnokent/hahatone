from flask import Flask
from flask import render_template, url_for, request, redirect, g, session
from flask_sqlalchemy import SQLAlchemy as sa
from sqlalchemy import select
from datetime import datetime
from flask import logging
from flask import flash
from setuptools import setup
from flask_login import login_manager
from flask_login import LoginManager
from flask_login import current_user, login_user
import os
import sqlite3 as sq

import json
import os

#ИМПОРТ ИЗ ДРУГИХ ФАЙЛОВ
from data import db_session
from data import schools
from data.schools import School
from data import people
from data.people import Person
from data import regions
from data.regions import Region
from data import students_points
from data.students_points import Student_point


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/base.db")

region = Region()
region.name = "random"
region.priz = 1
region.pobed = 1
region.members = 10
db_sess = db_session.create_session()
db_sess.add(region)
db_sess.commit()

if __name__ == "__main__":
    app.run(debug=True)