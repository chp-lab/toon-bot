import paho.mqtt.client as mqtt
from flask_restful import Resource, reqparse
from flask import request
from database import Database
from module import Module
import requests
from hooking import Hooking

class My_mqtt(Resource):
    topic = "@msg/set/status/"

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe(self.topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def unlock(self, room_num):
        TAG = "my_mqttinit:"
        # client_id = "12d62545-176c-4511-b3dc-61148c8e2a44"
        # token = "XxABgB71B2zssFGRcz3BrMZdJsb5G5TQ"
        # secret = "~#J0UDsDVyfkBBe$taZVetc3q-i_PL8_"
        # broker = "mqtt.netpie.io"
        port = 1883
        keep_alive = 60

        broker = "localhost"
        token = "chp-lab"
        secret = "atop3352"

        # client = mqtt.Client(client_id=client_id)
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.username_pw_set(token, secret)

        client.connect(broker, port, keep_alive)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        print(TAG, "mqtt start")
        print(TAG, "publish topic:" + self.topic + room_num, "payload:", "1")
        client.publish(self.topic + room_num, "1", qos=2)
        client.loop_start()
        print(TAG, "client stop")
        client.loop_stop()

    def post(self, room_num):
        TAG= "my_mqtt:"
        my_hooking = Hooking()
        onechat_uri = "https://chat-api.one.th"
        onechat_dev_token = "Bearer A1f52b98be0f25416a6a9a262d15747cbfa622f189173425aa8b8ba03bf8d67822a6ab46d22c34e21835d0ec2bb50240d"
        headers = {"Authorization": onechat_dev_token, "Content-Type": "application/json"}
        bot_id = "Bde6bcb263e82544ca9bae0d67b556ec4"

        module = Module()
        database = Database()

        auth_key = "Authorization"
        if(auth_key not in request.headers):
            return module.unauthorized()

        auth = request.headers.get("Authorization")
        print(TAG, "auth=", auth)
        # payload = {
        #     "bot_id":bot_id,
        #     "source":auth
        # }
        #
        # r = requests.post(onechat_uri + "/manage/api/v1/getprofile", headers=headers, json=payload)
        # print(TAG, "response code=", r.status_code)
        # # print(TAG, r.json())
        #
        # json_res = r.json()
        # print(TAG, "json_res=", json_res)

        guest_req_key = "guest_req"
        secret_key = "secret_key"
        parser = reqparse.RequestParser()

        parser.add_argument(guest_req_key)
        parser.add_argument(secret_key)

        args = parser.parse_args()
        guest_req = args.get(guest_req_key)
        secret = args.get(secret_key)
        print(TAG, "guest_req=", guest_req, "secret=", secret)

        if(guest_req != "checkin"):
            print(TAG, "you call apiin wrong way, guest_req=", guest_req)
            return module.wrongAPImsg()
        my_secret = "9qn1a2MTswD52m6PfU1kdLgfJK4NDoem!HRjRng!F_8AAv*c!*bOCLVxOSj9-XKZ"
        if(secret != my_secret):
            print(TAG, "You don't know the trust!")
            return module.unauthorized()

        print(TAG, "unlocking")
        self.unlock(room_num)
        print(TAG, "unlock complete")
        res = {
            "type": True,
            "message": "success",
            "error_message": None,
            "len": 1,
            "result": [
                {
                    "door": "open_success",
                    "one_email": "anonymouse",
                    "one_id": "anonymouse",
                    "nickname": "anonymouse"
                }
            ]
        }
        return res
        else:
            return module.unauthorized()

if (__name__ == "__main__"):
    my_mqtt = My_mqtt()