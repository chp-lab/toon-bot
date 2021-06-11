# -- coding: utf-8 --

from logging import log
from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Hooking(Resource):
    beaconbot_id = "B7f2abd3c4e0e57dbb5c71bfa43920b5a"
    onechat_uri = "https://chat-api.one.th"
    onechat_dev_token = "Bearer Af047823219745b05b6993360704664914fff808c0a544edfa73dbec65d8daebf59ea0ed141bd4d93811a798db510b5c8"
    onechat_url1 = onechat_uri + '/message/api/v1/push_quickreply'

    sendmessage_body ={}

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

        # print("this is data :" + json.dumps(data))

        # checkcovid_url = 'https://hr-management.inet.co.th:5000/detail_user_data'
        # checkcovid_body = {
        #                     "oneid": "12643514984"
        #                   }
        # checkcovid = requests.post(checkcovid_url, json=checkcovid_body, verify=False)
        # print("type of :" + str(type(checkcovid)))
        # print("this is transform : " + str(type(checkcovid.json())))
        # print("this is jsondump type : " + str(type(json.dumps(checkcovid.json()))))

        # print("this is covid result : " + json.dumps(checkcovid.json()))
        # print("len of covid result : " + json.dumps(len(checkcovid.json())))
        # print("debug onechat response :" + json.dumps(checkcovid.json()))
        # print(len(checkcovid))
        # [print(len(x)) for x in checkcovid]
        # [print(len(checkcovid))]
        # [print(x) for x in checkcovid]
        # if(checkcovid[127]["check_date"] == "2021-06-10" ):
	        # print(" Status Is "+ checkcovid[127]["status"])
        # print(len(checkcovid.text))
        # for i in range(len(checkcovid)):{
        #     print("i = ",i, "data is ",checkcovid.json[i])
        # }
        # print(checkcovid[]["check_date"])
        # if ("uuid" in data):
        #     print("this is one_id : " + data['oneid'])
        
        

        # if ('event' in data):
        #     print(data['event'])
        #     if(data['event'] == 'greeting'):
        #         print('this is greeting')

        if ('event' in data):
            print(data['event'])
            if(data["event"]=='message' and data['message']['text']=='Hi'):
                sendmessage_body = {
                                    "to":data['source']['one_id'],
                                    "bot_id": self.beaconbot_id,
                                    "type": "text",
                                    "message": "Say,Hi"+" "+data['source']['email'],
                                    "custom_notification": "ตอบกลับข้อความคุณครับ"
                                }
                sendmessage = requests.post(self.sendmessage_url, json=sendmessage_body, headers=self.sendmessage_headers, verify=False)
                print("debug onechat response :" + json.dumps(sendmessage.json()))

        # sendmessage_headers = {"Authorization": self.onechat_dev_token}
        # sendmessage_url = 'https://chat-api.one.th/message/api/v1/push_message'
        # sendmessage_body = {
        #                             "to": data['oneid'],
        #                             "bot_id": "B7f2abd3c4e0e57dbb5c71bfa43920b5a",
        #                             "type": "text",
        #                             "message": data['payload'],
        #                             "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
        # }
        # sendmessage = requests.post(sendmessage_url, json=sendmessage_body, headers=sendmessage_headers, verify=False)
        # print("debug onechat response :" + json.dumps(sendmessage.json()))

    #petdy_iBEACON
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

            # sendmessage_headers = {"Authorization": self.onechat_dev_token}
            # sendmessage_url = 'https://chat-api.one.th/message/api/v1/push_message'
            # sendmessage_body = {}
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
