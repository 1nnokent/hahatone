from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sq

app = Flask(__name__, template_folder="templates")
app.secret_key = 'super_secret_key'

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/students/<student_id>')
def student_page():
    return render_template('student.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
