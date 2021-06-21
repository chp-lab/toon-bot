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
    beaconbot_id = "Bde6bcb263e82544ca9bae0d67b556ec4"
    onechat_uri = "https://chat-api.one.th"
    onechat_dev_token = "Bearer A1f52b98be0f25416a6a9a262d15747cbfa622f189173425aa8b8ba03bf8d67822a6ab46d22c34e21835d0ec2bb50240d"

    server_unlock_uri = "http://127.0.0.1:5003"

    covid_api = "https://hr-management.inet.co.th:5000/detail_user_data"
    covid_body = {}

    get_userprofile_api = "http://127.0.0.1:5007/api/v1/get_userprofile"
    get_userprofile_body = {}

    check_in_api = "http://127.0.0.1:5007/api/v1/check_in"
    check_in_body = {}

    check_out_api = "http://127.0.0.1:5007/api/v1/check_out"
    check_out_body = {}

    sendmessage_headers = {"Authorization": onechat_dev_token}
    sendmessage_url = 'https://chat-api.one.th/message/api/v1/push_message'
    sendmessage_body = {}

    onechat_url1 = onechat_uri + '/message/api/v1/push_quickreply'
    unlock_api = server_unlock_uri + "/api/v1/unlock/"


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

    def is_oneid_exist(self, one_id):
        TAG = "is_oneid_exist:"
        cmd = """SELECT users.one_id FROM users WHERE users.one_id='%s' """ %(one_id)
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

    def record_to_log(self, one_id, event, area_id):
        TAG = "record_to_log:"
        database = Database()
        sql = """INSERT INTO `access_log` (`log_id`, `one_id`, `event`, `area_id`, `created_at`) 
        VALUES (NULL, '%s', '%s', %s, CURRENT_TIMESTAMP)""" %(one_id, event, area_id)
        insert = database.insertData(sql)
        return insert

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

    def get_area(self, major, minor):
        TAG = "get_are:"
        database = Database()
        cmd = """SELECT rooms.address FROM `rooms` WHERE rooms.minor=%s AND rooms.major=%s""" %(minor, major)
        res = database.getData(cmd)

        print(TAG, "res=", res)
        return res

    def is_area_exist(self, major, minor):
        TAG = "is_area_exist:"
        res = self.get_area(major, minor)
        if(res[0]['len'] == 0):
            return False
        else:
            return True

    def send_quick_reply(self, one_id, msg, payload):
        TAG = "send_quick_reply:"
        req_body = {
            "to":one_id,
            "bot_id": self.beaconbot_id,
            "message": "ให้ช่วยอะไรดี",
            "quick_reply": payload
        }

        result = requests.post(self.onechat_url1, json=req_body, headers=self.sendmessage_headers)
        return result

    def menu_send(self, one_id):
        TAG = "menu_send:"
        web_vue_url1 = "http://onesmartaccess.ddns.net:8081"
        msg = "ให้ช่วยอะไรดี"
        payload = [
                    {
                        "label": "การเข้างานของคุณ",
                        "type": "text",
                        "message": "ดูการเข้างานของฉัน",
                        "payload": "my_rec"
                    },
                    {
                        "label": "Admin",
                        "type": "link",
                        "url": web_vue_url1,
                        "sign": "false",
                        "onechat_token": "true"
                    }
                ]
        res = self.send_quick_reply(one_id, msg, payload)
        print(TAG, "res=", res)

    def get_my_rec(self, one_id):
        TAG = "get_my_rec:"
        database = Database()
        print(TAG, "get data")
        cmd = """SELECT timeattendance.check_in, timeattendance.date, timeattendance.checkin_at, rooms.address 
        FROM `timeattendance`
        LEFT JOIN rooms ON timeattendance.checkin_at=rooms.minor
        WHERE timeattendance.employee_code="%s" AND timeattendance.date=CURRENT_DATE""" %(one_id)
        res = database.getData(cmd)
        return res

    def get_onechat_token(self, auth):
        TAG = "get_onechat_token:"
        module = Module()
        onechat_token = auth.split()

        print(TAG, "auth=", auth)

        if(len(onechat_token) < 2):
            return module.wrongAPImsg()
        if(onechat_token[0] != "Bearer"):
            return module.wrongAPImsg()

        return {
                   'type': True,
                   'message': "success",
                   'error_message': None,
                   'result': [{'onechat_token': onechat_token[1]}]
               }, 200

    def get_onechat_profile(self, auth):
        TAG = "get_onechat_profile:"
        module = Module()
        print(TAG, "auth=", auth)
        payload = {
            "bot_id":  self.beaconbot_id,
            "source": auth
        }

        r = requests.post(self.onechat_uri + "/manage/api/v1/getprofile", headers=self.sendmessage_headers, json=payload)
        print(TAG, "response code=", r.status_code)
        # print(TAG, r.json())

        json_res = r.json()
        # print(TAG, "json_res=", json_res)
        if(json_res['status'] != "success"):
            return module.unauthorized()

        return {
                   'type': True,
                   'message': "success",
                   'error_message': None,
                   'result': [{'onechat_profie': json_res}]
               }, 200

    def is_admin(self, one_id):
        TAG = "is_admin:"
        dataabaase = Database()
        module = Module()

        if(not self.is_oneid_exist(one_id)):
            return module.userNotFound()

        cmd = """SELECT users.role FROM `users` WHERE users.one_id='%s'""" %(one_id)
        res = dataabaase.getData(cmd)

        role = res[0]['result'][0]['role']

        print(TAG, "role=", role)

        if(role is None):
            return False
        elif(role == "admin"):
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

        dev_uri = "http://localhost:5008/api/v1/hooking"

        # print(TAG, "forward to dev")
        # try:
        #     r = requests.post(dev_uri, json=data, verify=False)
        #     print(TAG, "forward status=", r.status_code)
        # except:
        #     print(TAG), "no connection found!"

        if ('event' in data):
            if(data["event"]=='message'):
                message_db = self.get_message(1)
                one_id = data['source']['one_id']
                dissplay_name = data['source']['display_name']

                recv_msg = data['message']['text']
                print(TAG, "recv_msg=", recv_msg)

                one_email = data['source']['email']
                if(not self.is_user_exist(one_email)):
                    add_user = self.add_new_user(one_email, dissplay_name, one_id)
                    print(TAG, "add=new_user=", add_user)
                    self.send_msg(one_id, "ยินดีให้บริการค่ะ")
                    return module.success()

                if('data' in data['message']):
                    recv_data = data['message']['data']
                    if(recv_data == "my_rec"):
                        # get time reccv of this user
                        res = self.get_my_rec(one_id)
                        if(res[0]['len'] == 0):
                            self.send_msg(one_id, "ไม่พบเวลาเข้างานของคุณ")
                            return module.measurementNotFound()
                        rec = res[0]['result'][0]
                        reply_msg = "เวลาเข้างานของคุณคือ %s %s สถานที่ %s" %(rec['check_in'], rec['date'], rec['address'])
                        self.send_msg(one_id, reply_msg)
                        return module.success()
                    return module.success()

                sendmessage_body = {
                                    "to":data['source']['one_id'],
                                    "bot_id": self.beaconbot_id,
                                    "type": "text",
                                    "message": message_db[0]['result'][0]['message'],
                                    "custom_notification": "ตอบกลับข้อความคุณครับ"
                                }
                sendmessage = requests.post(self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                self.menu_send(one_id)
                return module.success()

            elif(data["event"]=='add_friend'):
                one_id = data['source']['one_id']
                dissplay_name = data['source']['display_name']
                one_email = data['source']['email']
                if(not self.is_user_exist(one_email)):
                    add_user = self.add_new_user(one_email, dissplay_name, one_id)
                    print(TAG, "add=new_user=", add_user)
                    self.send_msg(one_id, "ขอบคุณที่เพิ่มเพื่อนค่ะ")
                return module.success()

        if('uuid' in data):
            print(TAG, "event=", data)
            one_id = data['oneid']
            event_stage = data['event_stage']
            lat = data['user_latitude']
            long = data['user_longitude']
            rssi = data["rssi"]
            proximity = data['proximity']
            print(TAG, "one_id=", one_id)

            if(one_id == ''):
                admin_one_id = "6271993808"
                self.send_msg(admin_one_id, "### system: problem with oneid")
                print(TAG, "### one id is blank ###")
                return module.serveErrMsg()
            tmp_msg = "event_stage:%s, proximity:%s, rssi:%s" %(data['event_stage'], data['proximity'], data['rssi'])
            r = self.send_msg(one_id, tmp_msg)
            print(TAG, "r=", r)
            major = data['major']
            minor = data['minor']

            if(not self.is_area_exist(major, minor)):
                self.send_msg(one_id, "ไม่พบพื้นที่ในระบบ major:%s minor:%s" %(major, minor))
                return module.success()

            covid_body = { "oneid": one_id }
            self.get_userprofile_body = {
                "oneid": one_id
            }
            user_profile = requests.post(self.get_userprofile_api, json=self.get_userprofile_body, verify=False)
            # print("this is user profile : "  + json.dumps(user_profile.json()["result"][0]["one_id"]))
            print(TAG, "user_profile=", user_profile)

            # daily = self.check_daily(one_id, datetime.today().strftime('%Y-%m-%d'))

            # record to access log
            if ((event_stage == 'enter') or (event_stage == 'immediate')):
                print(TAG, "record to access log")
                rec = self.record_to_log(one_id, event_stage, minor)

            if((event_stage == 'enter') or (event_stage == 'proximity_change')):
                # open the door

                print(TAG, "proximity=", proximity)
                if(proximity == "near"):
                    print(TAG, "user close to thee door, open the door")
                    # get room num
                    room_cmd = """SELECT rooms.room_num FROM rooms WHERE rooms.minor=%s""" %(minor)
                    room = database.getData(room_cmd)
                    # print(TAG, "room=", room)
                    room_num = room[0]['result'][0]['room_num']
                    print(TAG, "room_num=", room_num)
                    unlock_entry = self.unlock_api + "/" + room_num
                    secret_key = "XxABgB71B2zssFGRcz3BrMZdJsb5G5TQ~#J0UDsDVyfkBBe$taZVetc3q-i_PL8_ST3cETapN7KutBVHFJRxKd86Kj4DUeoGPR8p#HK5ykKx5fjcp03G)E2C_IMp*C9w"
                    unlock_header = {"Authorization": secret_key}
                    unlock_body = {
                        "guest_req":"checkin",
                        "secret_key":"9qn1a2MTswD52m6PfU1kdLgfJK4NDoem!HRjRng!F_8AAv*c!*bOCLVxOSj9-XKZ",
                        "one_id":one_id
                    }
                    unlock_res = requests.post(unlock_entry, json=unlock_body, headers=unlock_header, verify=False)
                    print(TAG, "unlock_res=", unlock_res)
                    self.send_msg(one_id, "เปิดประตู")
                # do slow job first
                if (self.is_entred(one_id) and (event_stage == 'enter')):
                    print(TAG, "user was enter")
                    building = self.get_area(major, minor)
                    greeting_msg = """ยินดีต้อนรับสู่ %s""" %(building[0]['result'][0]['address'])
                    self.send_msg(one_id, greeting_msg)
                    # end the job
                    return module.success()
                elif(self.is_entred(one_id) and (event_stage == 'proximity_change')):
                    # print(TAG, "user are in the area")
                    # self.send_msg(one_id, "you are in the area")
                    return module.success()

                chekcovid = requests.post(self.covid_api, json=covid_body, verify=False)
                print(TAG, "covid respoens code=", chekcovid.status_code)
                covid_filter = filter(self.date_filter, chekcovid.json())

                #check is it first time user enter the area
                if (self.is_entred(one_id)):
                    print(TAG, "user was enter")
                    building = self.get_area(major, minor)
                    greeting_msg = """ยินดีต้อนรับสู่ %s""" %(building[0]['result'][0]['address'])
                    self.send_msg(one_id, greeting_msg)
                    # end the job
                    return module.success()

                print(TAG, "first enter of the day")
                # check is record is entered

                covid_data = chekcovid.json().pop()
                print(TAG, "covid_data=", covid_data)

                building = self.get_area(major, minor)
                building_address = """%s""" % (building[0]['result'][0]['address'])

                for covid_status in covid_filter:
                    if covid_status['status'] != None:
                        self.check_in_body = {
                            "one_email": user_profile.json()["result"][0]["one_email"],
                            "one_id": user_profile.json()["result"][0]["one_id"],
                            "check_in_time": "CURRENT_TIME",
                            "covid_tracking": covid_status['status'],
                            "date": "CURRENT_DATE",
                            "minor": minor,
                            "lat": lat,
                            "long": long
                        }
                        insert_user = requests.post(self.check_in_api, json=self.check_in_body, verify=False)
                        print("this is insert_user :" + json.dumps(insert_user.json()))
                        message_db = self.get_message(2)
                        self.sendmessage_body = {
                                "to": one_id,
                                "bot_id": self.beaconbot_id,
                                "type": "text",
                                "message": message_db[0]['result'][0]['message'],
                                "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                        }

                        sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                        print("debug onechat response :" + json.dumps(sendmessage.json()))
                        self.sendmessage_body = {
                                "to": one_id,
                                "bot_id": self.beaconbot_id,
                                "type": "text",
                                "message": "สถานะ covid tracking ของคุณคือ :" + covid_status['status'],
                                "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                        }
                        sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                        print("debug onechat response :" + json.dumps(sendmessage.json()))

                        message_db = self.get_message(3)
                        print(message_db[0]['result'][0])

                        greeting_msg = """ยินดีต้อนรับสู่ %s""" % (building_address)
                        self.sendmessage_body = {
                                "to": one_id,
                                "bot_id": self.beaconbot_id,
                                "type": "text",
                                "message": message_db[0]['result'][0]['message'] + "\n" + greeting_msg,
                                "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                        }
                        sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                        print("debug onechat response :" + json.dumps(sendmessage.json()))
                        return module.success()

                        # sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                        # print("debug onechat response :" + json.dumps(sendmessage.json()))
                    elif covid_status['status'] == None:
                        message_db = self.get_message(4)
                        print(message_db[0]['result'][0])
                        self.sendmessage_body = {
                                "to": one_id,
                                "bot_id": self.beaconbot_id,
                                "type": "text",
                                "message": message_db[0]['result'][0]['message'],
                                "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                        }
                        sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                        print("debug onechat response :" + json.dumps(sendmessage.json()))

            elif data['event_stage'] == 'leave':
                self.check_out_body = {
                    "check_out_time": "CURRENT_TIME",
                    "one_id": user_profile.json()["result"][0]["one_id"],
                    "minor": minor
                }
                checkout = requests.post(self.check_out_api, json=self.check_out_body, verify=False)
                print("this is checkout :" + json.dumps(checkout.json()))
                rec = self.record_to_log(one_id, event_stage, minor)

                building = self.get_area(major, minor)
                building_address = """%s""" % (building[0]['result'][0]['address'])

                self.sendmessage_body = {
                        "to": one_id,
                        "bot_id": self.beaconbot_id,
                        "type": "text",
                        "message": "อย่าลืมรักษาระยะห่างและล้างมือบ่อยๆ นะคะ " + building_address,
                        "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                }
                sendmessage = requests.post(self.sendmessage_url, json=self.sendmessage_body, headers=self.sendmessage_headers, verify=False)
                print("debug onechat response :" + json.dumps(sendmessage.json()))

                return module.success()
        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }


