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

        condition = """TRUE """

        one_email = args.get("one_email")
        one_id = args.get("one_id")
        checkin_date = args.get("checkin_date")
        enter_before = args.get("enter_before")
        enter_after = args.get ("enter_after")
        out_before = args.get("out_before")
        out_after = args.get("out_after")
        checkin_area = args.get("checkin_area")
        checkout_area = args.get("checkout_area")
        covid_status = args.get("covid_status")

        if(one_email is not None):
            print(TAG, "search with one email like", one_email)
            condition = condition + """ AND timeattendance.one_email LIKE '%%%s%%' """ %(one_email)

        if(one_id is not None):
            print(TAG, "serach with one_id like", one_id)
            condition = condition + """ AND ttimeattendance.employee_code LIKE '%%%s%%' """ %(one_id)

        if(checkin_date is not None):
            print(TAG, "search with ddate")
            condition = condition + """ AND timeattendance.date=='%s' """ %(checkin_date)

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
