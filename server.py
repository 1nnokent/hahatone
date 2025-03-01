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

#база на алхимии
db_session.global_init("db/alch.db")





#БАЗА НА АЛХИМИИ
#Добавим известные регионы
db_sess = db_session.create_session()
db_sess.query(Region).filter(Region.id >= 0).delete()
db_sess.commit()
region = Region()
region.name = "Москва"
region.pobed = 0
region.priz = 0
region.members = 0
db_sess = db_session.create_session()
db_sess.add(region)
db_sess.commit()

region = Region()
region.name = "Санкт-Петербург"
region.pobed = 0
region.priz = 0
region.members = 0
db_sess = db_session.create_session()
db_sess.add(region)
db_sess.commit()

db_sess = db_session.create_session()
cnt = 0
for region in db_sess.query(Region).all():
    cnt += 1
    print(region.name)
print(cnt)

#массив всех людей
db_sess = db_session.create_session()
db_sess.query(School).filter(School.id >= 0).delete()
db_sess.commit()
db_sess = db_session.create_session()
db_sess.query(Person).filter(Person.id >= 0).delete()
db_sess.commit()
arr = []
with open('moscow.txt', 'r', encoding='utf-8') as f:
    count = 0
    #print('МОСКВА')
    for line in f:
        line = line.split(';')
        if count >= 1:
            place = line[0]
            full_name = line[1]
            full_name = full_name.split(" ")
            first_name = full_name[1]
            last_name = full_name[0]
            study_class = int(line[2])
            school_name = line[3]
            score = int(line[12])
            role = line[13]
            arr.append([first_name, last_name, study_class, school_name, score])
            #ДОБАВЛЕНИЕ В БАЗУ ШКОЛЫ
            school = School()
            school.name = school_name
            school.region = "Москва"
            school.place = 0
            school.priz = 0
            school.members = 0
            school.pobed = 0
            db_sess = db_session.create_session()
            db_sess.add(school)
            db_sess.commit()

            #ДОБАВЛЕНИЕ В БАЗУ ЧЕЛОВЕКА
            person = Person()
            person.school = school_name
            person.firstname = first_name
            person.lastname = last_name
            person.score = score
            person.role = 0
            person.place = place
            problems = [0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(4, 12):
                if line[i] != '' and line[i] != '.':
                    # print(int(line[i]), i)
                    problems[i - 4] += int(line[i])
                else:
                    problems[i - 4] += 0


            person.problem1 = problems[0]
            person.problem2 = problems[1]
            person.problem3 = problems[2]
            person.problem4 = problems[3]
            person.problem5 = problems[4]
            person.problem6 = problems[5]
            person.problem7 = problems[6]
            person.problem8 = problems[7]
            person.tour1 = person.problem1 + person.problem2 + person.problem3 + person.problem4
            person.tour2 = person.problem5 + person.problem6 + person.problem7 + person.problem8
            person.score = person.tour1 + person.tour2
            #region.members += 1
            if role == "победитель":
                person.role = 1
            if role == "призёр":
                person.role = 2
            db_sess = db_session.create_session()
            db_sess.add(person)
            db_sess.commit()
            #print(place, first_name, last_name, study_class, school, score, role)
        count += 1

with open('piter.txt', 'r', encoding='utf-8') as f:
    count = 0
    #print('ПИТЕР')
    for line in f:
        line = line.split(';')
        if count >= 1:
            place = line[0]
            full_name = line[1]
            g = full_name
            full_name = full_name.split(" ")
            first_name = full_name[1]
            last_name = full_name[0]
            study_class = ''
            s = full_name[3]
            school_name = ''
            h = -1
            k = -1
            n = -1
            nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
            for i in range(0, len(g)):
                if g[i] == '(':
                    h = i
                if g[i] == ',':
                    k = i
                if g[i] == 'к':
                    n = i
            for num in range(h + 1, k):
                school_name += g[num]
            study = ""
            for num in range(k + 2, n - 1):
                study += g[num]
            study_class = int(study)
            score = int(line[len(line) - 1])
            arr.append([first_name, last_name, study_class, school_name, score])
            # ДОБАВЛЕНИЕ В БАЗУ ШКОЛЫ
            school = School()
            school.name = school_name
            school.region = "Санкт-Петербург"
            school.place = 0
            school.priz = 0
            school.members = 0
            school.pobed = 0
            db_sess = db_session.create_session()
            db_sess.add(school)
            db_sess.commit()


            # ДОБАВЛЕНИЕ В БАЗУ ЧЕЛОВЕКА
            person = Person()
            person.school = school_name
            person.firstname = first_name
            person.lastname = last_name
            person.score = score
            person.place = place
            problems = [0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(2, 9):
                if line[i] != '' and line[i] != '.':
                    # print(int(line[i]), i)
                    problems[i - 2] += int(line[i])
                else:
                    problems[i - 2] += 0

            person.problem1 = problems[0]
            person.problem2 = problems[1]
            person.problem3 = problems[2]
            person.problem4 = problems[3]
            person.problem5 = problems[4]
            person.problem6 = problems[5]
            person.problem7 = problems[6]
            person.problem8 = problems[7]
            person.tour1 = person.problem1 + person.problem2 + person.problem3 + person.problem4
            person.tour2 = person.problem5 + person.problem6 + person.problem7 + person.problem8
            person.score = person.tour1 + person.tour2
            # У НИХ НЕ НАПИСАНО, ПОЭТОМУ ИЗМЕНЯТЬ НАДО БУДЕТ КАК-ТО ГДЕ-ТО ПОТОМ
            person.role = 0
            db_sess = db_session.create_session()
            db_sess.add(person)
            db_sess.commit()
            #print(place,first_name, last_name, study_class, school_name, score)
        count += 1
db_sess = db_session.create_session()
cnt = 0
for person in db_sess.query(Person).all():
    cnt += 1
    #print(person.firstname, person.lastname,person.school, person.score, person.role)
#print(cnt)


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
