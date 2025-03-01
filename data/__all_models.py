#МОДЕЛИ ДЛЯ РАБОТЫ С БАЗОЙ
from . import schools
from . import students
from . import regions
from . import students_points
from . import student_dop

#НА ВСЯКИЙ СЛУЧАЙ
from flask import Flask
from flask import render_template, url_for, request, redirect, g
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