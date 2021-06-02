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

    user_data = {
        "name": '',
        "employee_code": '',
        "check_in": '',
        "check_out": '',
        "covid_tracking":''
    }

    def date_filter(self, date):
        if date['check_date'] == datetime.today().strftime('%Y-%m-%d'):
            return True
        else:
            return False

    def post(self):
        TAG = "Hooking:"
        data = request.json
        print(TAG, "data=", data)
        print(TAG, request.headers)
        database = Database()
        module = Module()

        # # if(data['uuid'] == "C8A94F42-3CD5-483A-8ADC-97473197B8B4"):
        if('uuid' in data):
            print(data['oneid'])
            covid_body = { "oneid": data['oneid'] }

            chekcovid = requests.post(self.covid_api, json=covid_body, verify=False)
            print(type(chekcovid.json()))
            covid_filter = filter(self.date_filter, chekcovid.json())
            print(type(covid_filter))
            for covid_status in covid_filter:
                print('this is covid_filter : ' + json.dumps(covid_status))


            # for covid in chekcovid.json():
            #     if(covid["check_date"] == "2021-06-02"):
            #         print(covid)


        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
