import random
import string
import os

from flask import Flask, render_template, request
import sqlite3 as sq
from datetime import datetime

connect = sq.connect('/db/base.db', check_same_thread=False)
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
    sql_req = f"SELECT COUNT(*) FROM students WHERE role = '{role}'"
    result = sql_execute(sql_req)
    count = result.fetchone()[0]
    return count
    