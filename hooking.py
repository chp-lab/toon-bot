# -- coding: utf-8 --

from time import time
from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
import time
from threading import Timer
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Hooking(Resource):
    beaconbot_id = "Bde6bcb263e82544ca9bae0d67b556ec4"
    onechat_uri = "https://chat-api.one.th"
    onechat_dev_token = "Bearer A1f52b98be0f25416a6a9a262d15747cbfa622f189173425aa8b8ba03bf8d67822a6ab46d22c34e21835d0ec2bb50240d"

    covid_api = "https://hr-management.inet.co.th:5000/detail_user_data"
    covid_body = {}

    get_userprofile_api = "http://203.151.164.229:5007/api/v1/get_userprofile"
    get_userprofile_body = {}

    check_in_api = "http://203.151.164.229:5007/api/v1/check_in"
    check_in_body = {}

    check_out_api = "http://203.151.164.229:5007/api/v1/check_out"
    check_out_body = {}

    sendmessage_headers = {"Authorization": onechat_dev_token}
    sendmessage_url = 'https://chat-api.one.th/message/api/v1/push_message'
    sendmessage_body = {}

    request_count = []

    user_data = {
        "name": '',
        "employee_code": '',
        "check_in": '',
        "check_out": '',
        "covid_tracking":''
    }

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

    def get_message(self, key):
        print("this is KEY" + str(key))
        database = Database()
        sql = """SELECT message FROM bot_message WHERE bot_message.message_keys ='%d'""" %(key)
        message = database.getData(sql)
        return message

    def is_user_exist(self, one_email):
        TAG = "is_user_exist:"
        cmd = """SELECT users.one_email FROM users WHERE users.one_email='%s' """ %(one_email)
        database = Database()
        res = database.getData(cmd)
        print(TAG, "res=", res)
        if(res[0]['len'] > 0):
            return True
        else:
            return False

    def add_new_user(self, email, name, one_id):
        TAG = "add_new_user:"
        database = Database()
        print(TAG, "add user to our system")
        sql = """INSERT INTO `users` (`one_email`, `name`, `one_id`) VALUES ('%s', '%s', '%s')""" \
              % (email, name, one_id)
        insert = database.insertData(sql)
        return insert

    def delay(self):
        print("wait for check table . . .")

    def count_request(self, request_num):
        self.request_count.append(request_num)
        print("this is count_request len : " + str(len(self.request_count)))
        print(json.dumps(self.request_count))
        # do not delay in the server, must give good priority of the piece code
        # time.sleep(5)
        return self.request_count

    def check_sameUser(self, record):
        oneid_list = []
        newrecord_list = []

        for once_record in record:
            if newrecord_list.count(once_record) == 0 and oneid_list.count(once_record["oneid"]) == 0:
                oneid_list.append(once_record["oneid"])
                newrecord_list.append(once_record)

        print("this is oneid_list : " + json.dumps(oneid_list))
        print("this is newrecord_list : " + json.dumps(newrecord_list))
        return newrecord_list

    def beacon_ckeckin(self, data):
        record = self.count_request(data)
        print("this is record : " + json.dumps(record))
        self.request_count.clear()

    def send_msg(self, one_id, reply_msg):
        TAG = "send_msg:"

        payload = {
            "to": one_id,
            "bot_id": self.beaconbot_id,
            "type": "text",
            "message": reply_msg,
            "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
        }

        print(TAG, "payload=", payload)
        r = requests.post(self.sendmessage_url, json=payload, headers=self.sendmessage_headers, verify=False)

        return r

    def is_entred(self, one_id):
        TAG = "is_entered:"
        cmd = """SELECT timeattendance.log_id, timeattendance.one_email, timeattendance.check_in 
        FROM `timeattendance` 
        WHERE timeattendance.employee_code='%s' AND timeattendance.date=CURRENT_DATE""" %(one_id)
        database = Database()
        res = database.getData(cmd)
        print(TAG, res)
        if(res[0]['len'] == 0):
            return False
        else:
            return True

    def post(self):
        TAG = "Hooking:"
        data = request.json
        print(TAG, "data=", data)
        print(TAG, request.headers)
        database = Database()
        module = Module()

        if ('event' in data):
            if(data["event"]=='message'):
                message_db = self.get_message(1)
                sendmessage_body = {
                                    "to":data['source']['one_id'],
                                    "bot_id": self.beaconbot_id,
                                    "type": "text",
                                    "message": message_db[0]['result'][0]['message'],
                                    "custom_notification": "ตอบกลับข้อความคุณครับ"
                                }
                sendmessage = requests.post(self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                print("debug onechat response :" + json.dumps(sendmessage.json()))

            elif(data["event"]=='add_friend'):
                user_exist = self.is_user_exist(data['source']['email'])
                if(user_exist == False) :
                    add_user = self.add_new_user(data['source']['email'], data['source']['display_name'], data['source']['one_id'])
                    print(TAG, "add=new_user=", add_user)

        if('uuid' in data):
            print(TAG, "event=", data)
            one_id = data['oneid']
            tmp_msg = "event_stage:%s, proximity:%s" %(data['event_stage'], data['proximity'])
            r = self.send_msg(one_id, tmp_msg)
            print(TAG, "r=", r)
            # return

            if(self.is_user_exist(one_id)):
                print(TAG, "user was enter")
                return
            else:
                print(TAG, "first enter of the day")

            record = self.count_request(data)
            newdata =  self.check_sameUser(record)
            # self.request_count.clear()
            
            print("this is new data : " + json.dumps(newdata))
            covid_body = { "oneid": newdata[0]['oneid'] }
            self.get_userprofile_body = {
                "oneid": newdata[0]['oneid']
            }
            user_profile = requests.post(self.get_userprofile_api, json=self.get_userprofile_body, verify=False)
            print("this is user profile : "  + json.dumps(user_profile.json()["result"][0]["one_id"]))

            daily = self.check_daily(newdata[0]['oneid'], datetime.today().strftime('%Y-%m-%d'))

            if newdata[0]['event_stage'] == 'enter':
                # check is record is entered
                chekcovid = requests.post(self.covid_api, json=covid_body, verify=False)
                covid_filter = filter(self.date_filter, chekcovid.json())
                for covid_status in covid_filter:
                    if covid_status['status'] != None:
                        if daily[0]['len'] == 0:
                            self.check_in_body = {
                                "one_email": user_profile.json()["result"][0]["one_email"],
                                "one_id": user_profile.json()["result"][0]["one_id"],
                                "check_in_time": datetime.today().strftime("%H:%M:%S"),
                                "covid_tracking": covid_status['status'],
                                "date": datetime.today().strftime('%Y-%m-%d'),
                            }
                            insert_user = requests.post(self.check_in_api, json=self.check_in_body, verify=False)
                            print("this is insert_user :" + json.dumps(insert_user.json()))
                            message_db = self.get_message(2)
                            self.sendmessage_body = {
                                    "to": newdata[0]['oneid'],
                                    "bot_id": self.beaconbot_id,
                                    "type": "text",
                                    "message": message_db[0]['result'][0]['message'],
                                    "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                            }

                            sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                            print("debug onechat response :" + json.dumps(sendmessage.json()))
                            self.sendmessage_body = {
                                    "to": newdata[0]['oneid'],
                                    "bot_id": self.beaconbot_id,
                                    "type": "text",
                                    "message": "สถานะ covid tracking ของคุณคือ :" + covid_status['status'],
                                    "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                            }
                            sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                            print("debug onechat response :" + json.dumps(sendmessage.json()))

                            message_db = self.get_message(3)
                            print(message_db[0]['result'][0])
                            self.sendmessage_body = {
                                    "to": newdata[0]['oneid'],
                                    "bot_id": self.beaconbot_id,
                                    "type": "text",
                                    "message": message_db[0]['result'][0]['message'] + "\n" + 
                                            "---------------------------" + "\n" +
                                        "uuid : " + newdata[0]['uuid'] + "\n" +
                                        "major : " + newdata[0]['major'] + "\n" + 
                                        "minor : " + newdata[0]['minor'] + "\n" +
                                        "rssi : " + str(newdata[0]['rssi']) + "\n" +
                                        "event_stage : " + newdata[0]['event_stage'] + "\n" +
                                        "proximity :  " + newdata[0]['proximity'],
                                    "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                            }
                            sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                            print("debug onechat response :" + json.dumps(sendmessage.json()))

                        elif daily[0]['len'] == 1:
                            self.sendmessage_body = {
                                "to": newdata[0]['oneid'],
                                "bot_id": self.beaconbot_id,
                                "type": "text",
                                "message": "สวัสดี ตั้งใจทำงานค่ะ" + "\n" + 
                                            "---------------------------" + "\n" +
                                        "uuid : " + newdata[0]['uuid'] + "\n" +
                                        "major : " + newdata[0]['major'] + "\n" + 
                                        "minor : " + newdata[0]['minor'] + "\n" +
                                        "rssi : " + str(newdata[0]['rssi']) + "\n" +
                                        "event_stage : " + newdata[0]['event_stage'] + "\n" +
                                        "proximity :  " + newdata[0]['proximity'],
                                "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                        }
                        sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                        print("debug onechat response :" + json.dumps(sendmessage.json()))

                            
                    elif covid_status['status'] == None:
                        message_db = self.get_message(4)
                        print(message_db[0]['result'][0])
                        self.sendmessage_body = {
                                "to": newdata[0]['oneid'],
                                "bot_id": self.beaconbot_id,
                                "type": "text",
                                "message": message_db[0]['result'][0]['message']+ "\n" + 
                                            "---------------------------" + "\n" +
                                        "uuid : " + newdata[0]['uuid'] + "\n" +
                                        "major : " + newdata[0]['major'] + "\n" + 
                                        "minor : " + newdata[0]['minor'] + "\n" +
                                        "rssi : " + str(newdata[0]['rssi']) + "\n" +
                                        "event_stage : " + newdata[0]['event_stage'] + "\n" +
                                        "proximity :  " + newdata[0]['proximity'],
                                "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                        }
                        sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                        print("debug onechat response :" + json.dumps(sendmessage.json()))

            elif newdata[0]['event_stage'] == 'leave':
                print("this is Daily" + json.dumps(daily[0]['len']))
                if daily[0]['len'] != 0:
                        self.check_out_body = {
                            "check_out_time": datetime.today().strftime("%H:%M:%S"),
                            "one_id": user_profile.json()["result"][0]["one_id"]
                        }
                        checkout = requests.post(self.check_out_api, json=self.check_out_body, verify=False)
                        print("this is checkout :" + json.dumps(checkout.json()))

                        self.sendmessage_body = {
                                "to": newdata[0]['oneid'],
                                "bot_id": self.beaconbot_id,
                                "type": "text",
                                "message": "อย่าลืมรักษาระยะห่างและล้างมือบ่อยๆ นะคะ" + "\n" + 
                                            "---------------------------" + "\n" +
                                        "uuid : " + newdata[0]['uuid'] + "\n" +
                                        "major : " + newdata[0]['major'] + "\n" + 
                                        "minor : " + newdata[0]['minor'] + "\n" +
                                        "rssi : " + str(newdata[0]['rssi']) + "\n" +
                                        "event_stage : " + newdata[0]['event_stage'] + "\n" +
                                        "proximity :  " + newdata[0]['proximity'],
                                "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                        }
                        sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                        print("debug onechat response :" + json.dumps(sendmessage.json()))
        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }


