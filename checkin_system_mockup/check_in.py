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
    def is_entred(self, one_id):
        TAG = "is_entered:"
        cmd = """SELECT timeattendance.log_id, timeattendance.one_email, timeattendance.check_in 
        FROM `timeattendance` 
        WHERE timeattendance.employee_code='%s' AND timeattendance.date=CURRENT_DATE""" %(one_id)
        database = Database()
        res = database.getData(cmd)
        print(TAG, res)
        if(res[0]['len'] == 0):
            return False
        else:
            return True

    def check_in(self, one_email, one_id, check_in_time, covid_tracking, date):
        TAG = "check_in:"
        module = Module()
        if(self.is_entred(one_id)):
            print(TAG, "user was enter")
            # end job when record is exist!
            return module.wrongAPImsg()
        database = Database()
        sql = """INSERT INTO `timeattendance` (`one_email`, `employee_code`, `check_in`, `covid_tracking`, `date`) VALUES ('%s', '%s', '%s', '%s', '%s')""" \
              % (one_email, one_id, check_in_time, covid_tracking, date)
        insert = database.insertData(sql)
        return insert

    def post(self):
        result = self.check_in(request.json['one_email'],request.json['one_id'],request.json['check_in_time'],request.json['covid_tracking'],request.json['date'])
        return result