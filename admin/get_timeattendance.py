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
    def get_timeattendance(self, args):
        TAG = "get_timeattendan:"
        module = Module()

        condition = """True"""

        one_email_key  = "one_email"

        if(module.isQueryStr(args, one_email_key)):
            one_email = args.get(one_email_key)
            print(TAG, "search with one email like", one_email)
            condition = condition + """ AND timeattendance.one_email LIKE '%%%s%%' """ %(one_email)

        cmd = """SELECT timeattendance.log_id, timeattendance.one_email, timeattendance.employee_code, timeattendance.check_in, timeattendance.check_out, 
        timeattendance.covid_tracking, timeattendance.date, timeattendance.checkin_at AS this_checkin, timeattendance.checkout_at AS this_checkout,
        (SELECT rooms.room_num FROM rooms WHERE rooms.minor=this_checkin) AS checkin_area,
        (SELECT rooms.room_num FROM rooms WHERE rooms.minor=this_checkout) AS checkout_area,
        timeattendance.latitude, timeattendance.longitude
        FROM `timeattendance`
        WHERE %s
        ORDER BY `log_id`  DESC""" %(condition)



        database = Database()
        res = database.getData(cmd)
        return res

    def post(self):
        args = request.args
        timeattendance = self.get_timeattendance(args)
        return timeattendance

    def get(self):
        TAG = "get_timeatt:"
        module = Module()
        hooking = Hooking()

        auth_key = "Authorization"
        if(auth_key not in request.headers):
            return module.unauthorized()

        auth = request.headers.get("Authorization")

        res = hooking.get_onechat_token(auth)
        if(res[1] != 200):
            return res

        onechat_token = res[0]['result'][0]['onechat_token']

        prof_res = hooking.get_onechat_profile(onechat_token)
        print(TAG, "onechat_profile=", prof_res)
        if(prof_res[1] != 200):
            return prof_res

        one_id = prof_res[0]['result'][0]['onechat_profie']['data']['one_id']
        if(not hooking.is_admin(one_id)):
            return {
                       'type': False,
                       'message': "fail",
                       'error_message': "You are not admin",
                       'result': None
                   }, 401

        args = request.args

        timeattendance = self.get_timeattendance(args)

        return timeattendance
