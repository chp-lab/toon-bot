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


class Access_log(Resource):
    def get_access_log(self, args):
        TAG = "get_access_log:"
        database = Database()
        module = Module()

        condition = """TRUE """

        one_id = args.get("one_id")
        event = args.get("event")
        area_id = args.get("area_id")

        if(one_id is not None):
            print(TAG, "serach with one_id=", one_id)
            condition = condition + \
                """ AND access_log.one_id='%s' """ % (one_id)

        if(event is not None):
            print(TAG, "filter event status=", event)
            condition = condition + \
                """ AND access_log.event='%s' """ % (event)

        if(area_id is not None):
            print(TAG, "serach with area_id=", area_id)
            condition = condition + \
                """ AND access_log.area_id='%s' """ % (area_id)

        cmd = """SELECT access_log.one_id, access_log.event, access_log.area_id
        FROM `access_log`
        WHERE %s
        ORDER BY `log_id`  DESC""" % (condition)

        print("Command in search: ", cmd)

        res = database.getData(cmd)
        return res

    def get(self):
        TAG = "get_access_log:"
        module = Module()
        hooking = Hooking()

        auth_key = "Authorization"
        if(auth_key not in request.headers):
            return module.unauthorized()

        auth = request.headers.get("Authorization")

        res = hooking.get_onechat_token(auth)
        if(res[1] != 200):
            return res

        onechat_token = res[0]['result'][0]['onechat_token']

        prof_res = hooking.get_onechat_profile(onechat_token)
        print(TAG, "onechat_profile=", prof_res)
        if(prof_res[1] != 200):
            return prof_res

        one_id = prof_res[0]['result'][0]['onechat_profie']['data']['one_id']
        if(not hooking.is_admin(one_id)):
            return {
                'type': False,
                'message': "fail",
                'error_message': "You are not admin",
                'result': None
            }, 401

        args = request.args

        access_log = self.get_access_log(args)

        return access_log
