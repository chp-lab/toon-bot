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
        one_email = args.get("one_email")
        name = args.get("name")
        event = args.get("event")
        area = args.get("area")
        checkout_area = args.get("checkout_area")
        # area_id = args.get("area_id")

        if(one_id is not None):
            print(TAG, "serach with one_id=", one_id)
            condition = condition + \
                """ AND access_log.one_id='%s' """ % (one_id)

        if(one_email is not None):
            print(TAG, "search with one email like", one_email)
            condition = condition + \
                """ AND users.one_email LIKE '%%%s%%' """ % (
                    one_email)

        if(name is not None):
            print(TAG, "search with name like", name)
            condition = condition + \
                """ AND users.name LIKE '%%%s%%' """ % (
                    name)

        if(event is not None):
            print(TAG, "filter event status=", event)
            condition = condition + \
                """ AND access_log.event='%s' """ % (event)

        if(area is not None):
            print(TAG, "search with area like", area)
            condition = condition + \
                """ AND (rooms.room_num LIKE '%%%s%%' """ % (area) + \
                """OR rooms.building LIKE '%%%s%%' """ % (area) + \
                """OR rooms.address LIKE '%%%s%%') """ % (area)

        # if(area is not None):
        #     print(TAG, "area at like", area)
        #     area_cmd = """SELECT rooms.minor, rooms.room_num, rooms.address
        #     FROM rooms
        #     WHERE rooms.room_num LIKE '%%%s%%'""" % (area)

        #     matched_area = database.getData(area_cmd)

        #     print(TAG, "checkin matched_area=", matched_area)

        #     if(matched_area[0]['len'] > 0):
        #         areas = matched_area[0]['result']
        #         area_filter = ""
        #         for i in range(len(areas)):
        #             area_minor = areas[i]['minor']
        #             if(i == 0):
        #                 area_filter = "access_log.area_id=%s" % (
        #                     area_minor)
        #             else:
        #                 area_filter = area_filter + \
        #                     " OR access_log.area_id=%s" % (area_minor)
        #         condition = condition + """ AND (%s) """ % (area_filter)
        #     else:
        #         condition = condition + """ AND False """

        # if(area_id is not None):
        #     print(TAG, "serach with area_id=", area_id)
        #     condition = condition + \
        #         """ AND access_log.area_id='%s' """ % (area_id)

        cmd = """SELECT access_log.one_id, users.one_email, users.name, access_log.event, access_log.created_at, rooms.room_num, rooms.building, rooms.address
        FROM `access_log`
        LEFT JOIN users ON access_log.one_id=users.one_id
        LEFT JOIN rooms ON access_log.area_id=rooms.minor
        WHERE %s
        ORDER BY `log_id`  DESC""" % (condition)

        # print("Command in search: ", cmd)

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
