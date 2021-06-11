from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Userprofile(Resource):
    def get_userprofile(self, one_id):
        cmd = """SELECT one_email,one_id,name FROM users WHERE users.one_id='%s' """ %(one_id)
        database = Database()
        res = database.getData(cmd)
        return res

    def post(self):
        result = self.get_userprofile(request.json['oneid'])
        return result