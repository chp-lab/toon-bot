from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Timeattendance(Resource):
    def get_timeattendance(self):
        cmd = """SELECT timeattendance.log_id, timeattendance.one_email, timeattendance.employee_code, timeattendance.check_in, timeattendance.check_out, 
        timeattendance.covid_tracking, timeattendance.checkin_at AS this_in, timeattendance.checkout_at AS this_checkout,
        (SELECT rooms.room_num FROM rooms WHERE rooms.minor=this_in) AS check_in_at,
        (SELECT rooms.room_num FROM rooms WHERE rooms.minor=this_checkout)
        FROM `timeattendance` ORDER BY `log_id`  DESC"""
        
        database = Database()
        res = database.getData(cmd)
        return res

    def post(self):
        timeattendance = self.get_timeattendance()
        return timeattendance

