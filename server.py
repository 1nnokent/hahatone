from flask import Flask, render_template, request, redirect, url_for
import db_requests as dr
import algorithms as al
import sqlite3 as sq
import csv

app = Flask(__name__, template_folder="templates")
app.secret_key = 'dj09(WJF*(#WsoJ#*fs'

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
    data = dr.get_region_statistics(3)
    parsed = al.parse_region_statistics(data)
    return render_template('statistics_1_0.html', data=parsed)

@app.route('/statistics/3', methods=['GET', 'POST'])
def statistics_3_page():
    if request.method == 'GET':
        #получить данные всех пользователей из бд
        return render_template('statistics_3.html') #с данными
    else:
        #получить фильтры
        #получить данные, используя фильтры
        return render_template('statistics_3.html') #с данными

#массив всех людей
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
            school = line[3]
            score = int(line[12])
            role = line[13]
            arr.append([first_name, last_name, study_class, school, score])
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
            full_name = full_name.split(" ")
            first_name = full_name[1]
            last_name = full_name[0]
            study_class = full_name[4]
            s = full_name[3]
            school = s[1:len(s) - 1]
            score = int(line[len(line) - 1])
            arr.append([first_name, last_name, study_class, school, score])
            #print(place,first_name, last_name, study_class, school, score)
        count += 1

for row in arr:
    print(row)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
