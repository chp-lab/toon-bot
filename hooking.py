# -- coding: utf-8 --

from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Hooking(Resource):
    beaconbot_id = "B75f7822f3c3153c699d6599d9b196633"
    onechat_uri = "https://chat-api.one.th"
    onechat_dev_token = "Bearer A1f52b98be0f25416a6a9a262d15747cbfa622f189173425aa8b8ba03bf8d67822a6ab46d22c34e21835d0ec2bb50240d"

    covid_api = "https://hr-management.inet.co.th:5000/detail_user_data"
    covid_body = {}

    get_userprofile_api = "http://203.151.164.230:9977/api/get_user_by_oneid"
    get_userprofile_body = {}

    user_data = {
        "name": '',
        "employee_code": '',
        "check_in": '',
        "check_out": '',
        "covid_tracking":''
    }

    def get_userprofile(self, one_id):
        TAG = "is_user_exist:"
        cmd = """SELECT one_email,one_id,name FROM users WHERE users.one_id='%s' """ %(one_id)
        database = Database()
        res = database.getData(cmd)
        return res
        # print(TAG, "res=", res)
        # if(res[0]['len'] > 0):
        #     return True
        # else:
        #     return False

    def date_filter(self, date):
        if date['check_date'] == datetime.today().strftime('%Y-%m-%d'):
            return True
        else:
            return False

    def check_in(self, name, employee_code, check_in, check_out, covid_tracking):
        TAG = "check_in:"
        database = Database()
        sql = """INSERT INTO `timeattendance` (`one_email`, `employee_code`, `check_in`, `check_out`, `covid_tracking`) VALUES ('%s', '%s', '%s', '%s', '%s')""" \
              % (name, employee_code, check_in, check_out, covid_tracking)
        insert = database.insertData(sql)
        return insert

    def post(self):
        TAG = "Hooking:"
        data = request.json
        print(TAG, "data=", data)
        print(TAG, request.headers)
        database = Database()
        module = Module()

        # # if(data['uuid'] == "C8A94F42-3CD5-483A-8ADC-97473197B8B4"):
        if('uuid' in data):
            covid_body = { "oneid": data['oneid'] }
            self.get_userprofile_body = { "one_id":  data['oneid'] }
            userprofile = requests.post(self.get_userprofile_api, json=self.get_userprofile_body, verify=False)
            user_info = userprofile.json()['user_data']


            chekcovid = requests.post(self.covid_api, json=covid_body, verify=False)
            covid_filter = filter(self.date_filter, chekcovid.json())
            print(type(covid_filter))
            for covid_status in covid_filter:
                print(77777)
                print(covid_status)
                if covid_status['status'] != None:
                    if 'green'in covid_status['status']:
                        user_profile = self.get_userprofile(data['oneid'])
                        check_in = self.check_in(json.dumps(user_info[0]['oneemail']), json.dumps(user_info[0]['oneid']), datetime.today().strftime('%Y-%m-%d'), datetime.today().strftime('%Y-%m-%d'), covid_status['status'])
                        print(TAG, "check_in", check_in)
                elif covid_status['status'] == None:
                    print('wtf!!! covid tracking nowwww')

                


        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
