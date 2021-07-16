from hooking import Hooking
from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Room_number(Resource):
    def get_room_number(self, args):
        TAG = "get_room_number:"
        database = Database()
        condition = """TRUE """

        room_number = args.get("room_number")

        if(room_number is not None):
            print(TAG, "search with room number like", room_number)
            condition = condition + \
                """ AND rooms.room_num LIKE '%%%s%%' """ % (room_number)

        cmd = """SELECT rooms.room_num
        FROM `rooms`
        WHERE %s
        """ % (condition)

        print("Command in search: ", cmd)

        res = database.getData(cmd)
        return res

    def get(self):
        # TAG = "get_room_number:"
        # module = Module()
        # hooking = Hooking()

        # auth_key = "Authorization"
        # if(auth_key not in request.headers):
        #     return module.unauthorized()

        # auth = request.headers.get("Authorization")

        # res = hooking.get_onechat_token(auth)
        # if(res[1] != 200):
        #     return res

        # onechat_token = res[0]['result'][0]['onechat_token']

        # prof_res = hooking.get_onechat_profile(onechat_token)
        # print(TAG, "onechat_profile=", prof_res)
        # if(prof_res[1] != 200):
        #     return prof_res

        # one_id = prof_res[0]['result'][0]['onechat_profie']['data']['one_id']
        # if(not hooking.is_admin(one_id)):
        #     return {
        #         'type': False,
        #         'message': "fail",
        #         'error_message': "You are not admin",
        #         'result': None
        #     }, 401

        args = request.args

        room_number = self.get_room_number(args)

        return room_number
