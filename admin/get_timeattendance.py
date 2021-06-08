from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Admin(Resource):
    def get_timeattendance(self):
        cmd = """SELECT * FROM users""" 
        database = Database()
        res = database.getData(cmd)
        return res

    def post(self):
        timeattendance = self.get_timeattendance()
        print("this is result" + json.dumps(timeattendance))
        return {
            'status': 200
        }
