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
    def update_checkout(self, time, one_id, minor):
        database = Database()
        sql = """UPDATE timeattendance 
        SET timeattendance.check_out = '%s', timeattendance.checkout_at=%s, timeattendance.updated_at=CURRENT_TIMESTAMP
        WHERE timeattendance.employee_code='%s' AND timeattendance.date=CURRENT_DATE""" \
              % (time, minor, one_id)
        update = database.insertData(sql)
        return update

    def post(self):
        result = self.update_checkout(request.json['check_out_time'], request.json['one_id'], request.json['minor'])
        return result