from flask import Flask, render_template, request, redirect, url_for
import db_requests as dr
import algorithms as al
import sqlite3 as sq

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
def statistics_1_page():
    data = dr.get_region_statistics(0)
    parsed = al.parse_region_statistics(data)
    return render_template('statistic_1_0', data=parsed)

@app.route('/statistics/1_1')
def statistics_1_page():
    data = dr.get_region_statistics(1)
    parsed = al.parse_region_statistics(data)
    return render_template('statistic_1_0', data=parsed)

@app.route('/statistics/1_2')
def statistics_1_page():
    data = dr.get_region_statistics(2)
    parsed = al.parse_region_statistics(data)
    return render_template('statistic_1_0', data=parsed)

@app.route('/statistics/1_3')
def statistics_1_page():
    data = dr.get_region_statistics(3)
    parsed = al.parse_region_statistics(data)
    return render_template('statistic_1_0', data=parsed)

@app.route('/statistics/3', methods=['GET', 'POST'])
def statistics_3_page():
    if request.method == 'GET':
        #получить данные всех пользователей из бд
        return render_template('statistics_3.html') #с данными
    else:
        #получить фильтры
        #получить данные, используя фильтры
        return render_template('statistics_3.html') #с данными


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
