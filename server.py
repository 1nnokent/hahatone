import string

from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import db_requests as dr
import algorithms as al
import csv
import matplotlib
matplotlib.use('Agg')  # Используем 'Agg' для headless-режима
import matplotlib.pyplot as plt
import io

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

import json
import os
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

app = Flask(__name__, template_folder="templates")
app.secret_key = 'dj09(WJF*(#WsoJ#*fs'



#ИМПОРТ ИЗ ДРУГИХ ФАЙЛОВ(для базы на алхимии)
from data import db_session
from data import students
from data.students import Person
from data import schools
from data.schools import School
from data import regions
from data.regions import Region
from data import student_dop
from data.student_dop import Person_dop

#база на алхимии
db_session.global_init("db/alch.db")




#ОСТАЛЬНОЙ КОД

def generate_score_plot(student_id):
    # Данные для графика
    rounds = {
        1: [(0, 0), (50, 60), (100, 120), (150, 180), (200, 240), (250, 300)],
        2: [(0, 0), (60, 70), (120, 140), (180, 210), (240, 270), (300, 320)]
    }

    plt.figure(figsize=(12, 10))
    for round_number, points in rounds.items():
        times, scores = zip(*points)
        plt.plot(times, scores, marker='o', linestyle='-', label=f'Тур {round_number}')

    plt.xlabel("Время (минуты)")
    plt.ylabel("Баллы")
    plt.title("Зависимость набранных баллов от времени")
    plt.legend()
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

@app.route('/plot.png/<int:student_id>')
def plot_png(student_id):
    img = generate_score_plot(student_id)
    response = make_response(send_file(img, mimetype='image/png'))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/students/<student_id>')
def student_page(student_id):
    student_data = dr.get_student_data(student_id)
    return render_template('student.html', student=student_data)


@app.route('/statistics/1_0')
def statistics_1_0():
    data_raw = dr.get_region_statistics(0)
    parsed = al.parse_region_statistics(data_raw)
    print(parsed)
    return render_template('statistics_1_0.html', data=parsed)

@app.route('/statistics/1_1')
def statistics_1_1():
    data = dr.get_region_statistics(1)
    parsed = al.parse_region_statistics(data)
    return render_template('statistics_1_0.html', data=parsed)

@app.route('/statistics/1_2')
def statistics_1_2():
    data = dr.get_region_statistics(2)
    parsed = al.parse_region_statistics(data)
    return render_template('statistics_1_0.html', data=parsed)

@app.route('/statistics/1_3')
def statistics_1_3():
    data = dr.get_region_statistics(1) + dr.get_region_statistics(2)
    parsed = al.parse_region_statistics(data)
    return render_template('statistics_1_0.html', data=parsed)

@app.route('/statistics/3', methods=['GET', 'POST'])
def statistics_3_page():
    stds = dr.get_students()
    parsed = al.parse_students(stds)
    return render_template('statistics_3.html', data=parsed)

if __name__ == '__main__':
    print(al.parse_second_tour('30.html'))
    app.run(port=8080, host='127.0.0.1')
