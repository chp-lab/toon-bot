from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Check_in(Resource):
    def check_in(self, one_email, one_id, check_in_time, covid_tracking, date):
        database = Database()
        sql = """INSERT INTO `timeattendance` (`one_email`, `employee_code`, `check_in`, `covid_tracking`, `date`) VALUES ('%s', '%s', '%s', '%s', '%s')""" \
              % (one_email, one_id, check_in_time, covid_tracking, date)
        insert = database.insertData(sql)
        return insert

    def post(self):
        result = self.check_in(request.json['one_email'],request.json['one_id'],request.json['check_in_time'],request.json['covid_tracking'],request.json['date'])
        return result