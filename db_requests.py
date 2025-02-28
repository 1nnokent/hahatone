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


def get_region_statistic(role):
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
    personal_info = sql_execute(sql_req1)
    sql_req2 = f"""
        SELECT 
            score
        FROM
            students_points
        WHERE
            student_id = {student_id}
    """
    points = sql_execute(sql_req2)
    ret = (personal_info, points)
    return ret