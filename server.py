from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
import db_requests as dr
import sqlite3 as sq
import matplotlib
matplotlib.use('Agg')  # Используем 'Agg' для headless-режима
import matplotlib.pyplot as plt
import io

app = Flask(__name__, template_folder="templates")
app.secret_key = 'dj09(WJF*(#WsoJ#*fs'

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
    print(student_data)
    return render_template('student.html', student=student_data, student_id=student_id)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

