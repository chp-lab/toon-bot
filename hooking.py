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
            covid_body = { "oneid": data['oneid'] }

            chekcovid = requests.post(self.covid_api, json=covid_body, verify=False)
            covid_filter = filter(self.date_filter, chekcovid.json())
            for covid_status in covid_filter:
                self.user_data['covid_tracking'] = json.dumps(covid_status['status'])
                print('this is user_data : ' + json.dumps(self.user_data))
                print(json.dumps(self.user_data['covid_tracking']))

        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
