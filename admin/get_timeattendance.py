from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from hooking import Hooking

class Timeattendance(Resource):
    def get_timeattendance(self):
        cmd = """SELECT timeattendance.log_id, timeattendance.one_email, timeattendance.employee_code, timeattendance.check_in, timeattendance.check_out, 
        timeattendance.covid_tracking, timeattendance.date, timeattendance.checkin_at AS this_checkin, timeattendance.checkout_at AS this_checkout,
        (SELECT rooms.room_num FROM rooms WHERE rooms.minor=this_checkin) AS checkin_area,
        (SELECT rooms.room_num FROM rooms WHERE rooms.minor=this_checkout) AS checkout_area,
        timeattendance.latitude, timeattendance.longitude
        FROM `timeattendance` ORDER BY `log_id`  DESC"""

        database = Database()
        res = database.getData(cmd)
        return res

    def post(self):
        timeattendance = self.get_timeattendance()
        return timeattendance

    def get(self):
        TAG = "get_timeatt:"
        module = Module()
        hooking = Hooking()

        timeattendance = self.get_timeattendance()

        auth_key = "Authorization"
        if(auth_key not in request.headers):
            return module.unauthorized()

        auth = request.headers.get("Authorization")
        onechat_token = auth.split()

        print(TAG, "auth=", auth)
        
        if(len(onechat_token) < 2):
            return module.wrongAPImsg()
        if(auth[0] != "Bearer"):
            return module.wrongAPImsg()

        hooking.get_onechat_profile(onechat_token[1])

        return timeattendance
