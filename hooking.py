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
    beaconbot_id = "B790a5e0089415d289d064cff06db374a"
    onechat_uri = "https://chat-api.one.th"
    onechat_dev_token = "Bearer A1f52b98be0f25416a6a9a262d15747cbfa622f189173425aa8b8ba03bf8d67822a6ab46d22c34e21835d0ec2bb50240d"

    covid_api = "https://hr-management.inet.co.th:5000/detail_user_data"
    covid_body = {}

    get_userprofile_api = "http://203.151.164.230:9977/api/get_user_by_oneid"
    get_userprofile_body = {}

    sendmessage_headers = {"Authorization": onechat_dev_token}
    sendmessage_url = 'https://chat-api.one.th/message/api/v1/push_message'
    sendmessage_body = {}

    user_data = {
        "name": '',
        "employee_code": '',
        "check_in": '',
        "check_out": '',
        "covid_tracking":''
    }

    def get_userprofile(self, one_id):
        cmd = """SELECT one_email,one_id,name FROM users WHERE users.one_id='%s' """ %(one_id)
        database = Database()
        res = database.getData(cmd)
        return res

    def check_daily(self, one_id, today):
        cmd = """SELECT * FROM timeattendance WHERE timeattendance.employee_code='%s' AND timeattendance.date='%s' """ %(one_id, today)
        database = Database()
        res = database.getData(cmd)
        return res

    def date_filter(self, date):
        if date['check_date'] == datetime.today().strftime('%Y-%m-%d'):
            return True
        else:
            return False

    def check_in(self, name, employee_code, check_in, covid_tracking):
        database = Database()
        sql = """INSERT INTO `timeattendance` (`one_email`, `employee_code`, `check_in`, `covid_tracking`) VALUES ('%s', '%s', '%s', '%s')""" \
              % (name, employee_code, check_in, covid_tracking)
        insert = database.insertData(sql)
        return insert

    def insert_record(self, one_email, one_id, check_in, date):
        database = Database()
        sql = """INSERT INTO `timeattendance` (`one_email`, `employee_code`, `check_in`, `date`) VALUES ('%s', '%s', '%s', '%s')""" \
              % (one_email, one_id, check_in, date)
        insert = database.insertData(sql)
        return insert

    def update_checkout(self, time, one_id):
        database = Database()
        sql = """UPDATE timeattendance SET check_out = '%s' WHERE timeattendance.employee_code='%s'""" \
              % (time, one_id)
        update = database.insertData(sql)
        return update

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
            user_profile = self.get_userprofile(data['oneid'])

            daily = self.check_daily(data['oneid'], datetime.today().strftime('%Y-%m-%d'))
            if daily[0]['len'] == 0:
                insert_user = self.insert_record(user_profile[0]['result'][0]['one_email'], user_profile[0]['result'][0]['one_id'], datetime.today().strftime("%H:%M:%S"), datetime.today().strftime('%Y-%m-%d'))
                print("this is insert_user :" + json.dumps(insert_user))
            elif daily[0]['len'] != 0:
                if data['event_stage'] == 'leave':
                    checkout = self.update_checkout(datetime.today().strftime("%H:%M:%S"), data['oneid'])
                    print("this is checkout :" + json.dumps(checkout))

                

            # chekcovid = requests.post(self.covid_api, json=covid_body, verify=False)
            # covid_filter = filter(self.date_filter, chekcovid.json())
            # for covid_status in covid_filter:
            #     if covid_status['status'] != None:
            #         checkin_status = self.get_checkin(data['oneid'])
            #         if checkin_status[0]['result'][0]['check_in'] == None:
            #             user_profile = self.get_userprofile(data['oneid'])
            #             check_in = self.check_in(user_profile[0]['result'][0]['one_email'], user_profile[0]['one_id'], datetime.today().strftime('%Y-%m-%d'), covid_status['status'])
            #             print(TAG, "check_in", check_in)

            #             self.sendmessage_body = {
            #                             "to": data['oneid'],
            #                             "bot_id": self.beaconbot_id,
            #                             "type": "text",
            #                             "message": "ลงเวลาเข้างานเรียบร้อยแล้ว" + "\n" +
            #                                         "สถานะ covid tracking ของคุณคือ :" + covid_status['status'],
            #                             "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
            #             }

            #             sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
            #             print("debug onechat response :" + json.dumps(sendmessage.json()))


            #     elif covid_status['status'] == None:
            #         print('wtf!!! covid tracking nowwww')

                
        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
