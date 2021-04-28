# -- coding: utf-8 --

from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Hooking(Resource):
    beaconbot_id = "B75f7822f3c3153c699d6599d9b196633"
    onechat_uri = "https://chat-api.one.th"
    
    onechat_dev_token = "Bearer A1f52b98be0f25416a6a9a262d15747cbfa622f189173425aa8b8ba03bf8d67822a6ab46d22c34e21835d0ec2bb50240d"

    onechat_url1 = onechat_uri + '/message/api/v1/push_quickreply'
    def menu_send(self, user_id, bot_id):
        TAG = "menu_send:"
        # web_vue_url1 = "https://web-meeting-room.herokuapp.com/"
        web_vue_url1 = "https://onesmartaccess.herokuapp.com/"
        req_body = {
            "to": user_id,
            "bot_id": bot_id,
            "message": "ให้ช่วยอะไรดี",
            "quick_reply":
                [
                    {
                        "label": "อัพโหลดรูป",
                        "type": "text",
                        "message": "อัพโหลดรูป",
                        "payload": {"action": "image_rec"}
                    },
                    {
                        "label": "ทำความรู้จักผู้คน",
                        "type": "text",
                        "message": "มีใครโสดอยู่บ้าง",
                        "payload": {"action": "find_single"}
                    },
                    {
                        "label": "อัพเดทโปรไฟล์",
                        "type": "text",
                        "message": "ขออัพเดทโปรไฟล์หน่อยครับ",
                        "payload": {"action": "profile_update"}
                    }
                ]
        }
        headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
        result = requests.post(self.onechat_url1, json=req_body, headers=headers)
        print(TAG, result.text)

    def post(self):
        TAG = "Hooking:"
        data = request.json
        print(TAG, "data=", data)
        print(TAG, request.headers)

        database = Database()
        module = Module()
        # onechat_uri = self.onechat_uri
        data = request.json
        # onechat_dev_token = "Bearer Af58c5450f3b45c71a97bc51c05373ecefabc49bd2cd94f3c88d5b844813e69a17e26a828c2b64ef889ef0c10e2aee347"
        # headers = {"Authorization": onechat_dev_token}

        print(TAG, "data=", data)
        # print(TAG, request.headers)
        print('********************************')

        # if('event' not in data):
        #     print(TAG, "event not found!")
        #     # assum OneChat iBeacon event detected
        #     print(TAG, "OneChat iBeacon detected")
        #     return module.success()
        #     # return module.wrongAPImsg()

        if('uuid' in data):
            print(TAG, data['uuid'])

            # getprofile_url = 'https://petdy-dev.one.th/api/get_user_by_oneid'
            # getprofile_body = {'one_id': data['oneid']}

            # result = requests.post(getprofile_url, json=getprofile_body, verify=False)
            # userprofile = result.json()['user_data'][0]

            # print(TAG, userprofile)
            # print(TAG, userprofile['oneid'])
            # print(TAG, userprofile['id'])

            sendmessage_headers = {"Authorization": self.onechat_dev_token}
            sendmessage_url = 'https://chat-api.one.th/message/api/v1/push_message'
            if data['platform'] === "ios":
                sendmessage_body = {
                                        "to": data['oneid'],
                                        "bot_id": self.beaconbot_id,
                                        "type": "text",
                                        "message": "สวัสดี" + "\n" + 
                                                "scan success !!" + "\n" +
                                                "---------------------------" + "\n" +
                                                "uuid : " + data['uuid'] + "\n" +
                                                "major : " + data['major'] + "\n" + 
                                                "minor : " + data['minor'] + "\n" +
                                                "rssi : " + str(data['rssi']) + "\n" ,
                                        "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                                    }
            if data['platform'] === "ios":
                sendmessage_body = {
                                    "to": data['oneid'],
                                    "bot_id": self.beaconbot_id,
                                    "type": "text",
                                    "message": "สวัสดี" + "\n" + 
                                               "scan success !!" + "\n" +
                                               "---------------------------" + "\n" +
                                               "uuid : " + data['uuid'] + "\n" +
                                               "major : " + data['major'] + "\n" + 
                                               "minor : " + data['minor'] + "\n" +
                                               "rssi : " + str(data['rssi']) + "\n" +
                                               "event_stage : " + data['event_stage '] + "\n",
                                    "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                                }

            sendmessage = requests.post(sendmessage_url, json=sendmessage_body, headers=sendmessage_headers, verify=False)
            print(sendmessage.json())


            # add_collar = self.add_new_pair(data['uuid'], userprofile['oneid'], userprofile['id'])
            # print('++++++++++++++++++++++++++++++++++++++++++')

       

        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
