from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Check_out(Resource):
    def update_checkout(self, time, one_id):
        database = Database()
        sql = """UPDATE timeattendance SET check_out = '%s' WHERE timeattendance.employee_code='%s'""" \
              % (time, one_id)
        update = database.insertData(sql)
        return update

    def post(self):
        result = self.update_checkout(request.json['time'], request.json['one_id'])
        return result