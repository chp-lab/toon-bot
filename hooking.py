# -- coding: utf-8 --

from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Hooking(Resource):
    beaconbot_id = "B75f7822f3c3153c699d6599d9b196633"
    onechat_uri = "https://chat-api.one.th"
    onechat_dev_token = "Bearer A1f52b98be0f25416a6a9a262d15747cbfa622f189173425aa8b8ba03bf8d67822a6ab46d22c34e21835d0ec2bb50240d"

    sendmessage_headers = {"Authorization": onechat_dev_token}
    sendmessage_url = 'https://chat-api.one.th/message/api/v1/push_message'
    sendmessage_body = {}

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

        if('event' in data):
            if(data['event'] == 'message'):
                sendmessage_body = {
                                        "to": data['source']['one_id'],
                                        "bot_id": self.beaconbot_id,
                                        "type": "text",
                                        "message": "I'm here for you ~",
                                        "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                                    }
                sendmessage = requests.post(self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                print("debug onechat response :" + json.dumps(sendmessage.json()))


        if('uuid' in data):
            
            # update_url = 'https://petdy-dev.one.th/api/beacon_update_location'
            # update_body = {
            #                     "event_stage":data['event_stage'],
            #                     "major":data['major'],
            #                     "minor":data['minor'],
            #                     "platform":data['platform'],
            #                     "rssi":data['rssi'],
            #                     "timestamp":data['timestamp'],
            #                     "user_latitude":data['user_latitude'],
            #                     "user_longitude":data['user_longitude'],
            #                     "uuid":data['uuid']
            #               }
            # print(update_body)
            # update = requests.post(update_url, json=update_body, verify=False)
            # print("updateLocation response :" + json.dumps(update.json()))

            
            if 'android' in data['platform']:
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
                                               "event_stage : " + data['event_stage'],
                                        "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                                    }
            if 'ios' in data['platform']:
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
                                               "rssi : " + data['rssi'] + "\n" +
                                               "event_stage : " + data['event_stage'],
                                    "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
                                }
            sendmessage = requests.post(self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
            print("debug onechat response :" + json.dumps(sendmessage.json()))

        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
