import random
import string
import os
from flask import Flask, render_template, request
import sqlite3 as sq
from datetime import datetime

connect = sq.connect('db/base.db', check_same_thread=False)
cursor = connect.cursor()

def sql_execute(sql_request):
    ret = cursor.execute(sql_request)
    return ret

def get_school(first_name, middle_name, second_name):
    sql_req = f"""
        SELECT
            school_name, region_name
        FROM
            schools INNER JOIN regions 
            ON school_region_id = region_id
            INNER JOIN students
            ON students.school_id = schools.school_id
        WHERE
            first_name = {first_name} 
            AND middle_name = {middle_name} 
            AND second_name = {second_name}  
    """
    return sql_execute(sql_req)


def get_region_statistics(role):
    sql_req = f"""
        SELECT 
            region_name, COUNT(*) 
        FROM 
            students INNER JOIN schools 
            ON students.school_id = schools.school_id 
            INNER JOIN regions 
            ON schools.school_region_id = regions.region_id 
        WHERE 
            category = '{role}' 
        GROUP BY region_name
    """
    result = sql_execute(sql_req)
    return result.fetchall()


def get_student_data(student_id):
    sql_req1 = f"""
        SELECT 
            first_name, middle_name, last_name, score, category, school_name
        FROM
            students INNER JOIN schools
            ON students.school_id = schools.school_id
        WHERE
            student_id = {student_id}
    """
    personal_info = sql_execute(sql_req1).fetchall()
    sql_req2 = f"""
        SELECT 
            score
        FROM
            students_points
        WHERE
            student_id = {student_id}
    """
    points = sql_execute(sql_req2).fetchall()
    ret = (personal_info, points)
    return ret


def get_student_place(student_id):
    sql_req = f"""
        SELECT 
            student_id, score
        FROM 
            students
        ORDER BY
            score DESC
    """
    result = sql_execute(sql_req)
    students = result.fetchall()

    ranked = []
    prev_score = None
    current_group_start = 0

    for i, (_, score) in enumerate(students):
        if score != prev_score:
            if prev_score is not None:
                ranked.append((current_group_start, i - 1))
            current_group_start = i
            prev_score = score
    ranked.append((current_group_start, len(students) - 1))

    for idx, (s_id, _) in enumerate(students):
        if s_id == student_id:
            for start, end in ranked:
                if start <= idx <= end:
                    if start == end:
                        return start + 1
                    else:
                        return f"{start + 1}-{end + 1}"
    return None


def get_students():
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
    return arr

def initialize():
    stds = get_students()
    print(stds)
    id = 0
    for elem in stds:
        sql_req = f"""
            INSERT INTO
                students
            VALUES
                ({id}, '{elem[0]}', NULL, '{elem[1]}', '{elem[2]}', {elem[4]}, {random.randint(0, 2)}, 0)
        """
        print(sql_req)
        sql_execute(sql_req)
        id += 1
    connect.commit()

#СОСТАВЛЕНИЕ БАЗЫ
'''
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

all_schools = []

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
            if len(all_schools) == 0 or all_schools.count(school_name) == 0:
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
                all_schools.append(school_name)

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
            all_schools = []
            if len(all_schools) == 0 or all_schools.count(school_name) == 0:
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
                all_schools.append(school_name)


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
for school in db_sess.query(School).all():
    cnt += 1
    print(school.name)
print(cnt)

'''
if __name__ == '__main__':
    print(get_school('Тимофей', None, 'Ижицкий'))