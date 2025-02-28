from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sq

app = Flask(__name__, template_folder="templates")
app.secret_key = 'dj09(WJF*(#WsoJ#*fs'

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/students/<student_id>')
def student_page():
    kwargs = dict()
    return render_template('student.html', **kwargs)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
