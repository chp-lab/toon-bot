from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Custommessage(Resource):
    def edit_message(self, key, message):
        database = Database()
        sql = """UPDATE bot_message SET message = '%s' WHERE bot_message.message_keys='%d'""" \
              % (message, key)
        update = database.insertData(sql)
        return update

    def post(self):
        edit_message = self.edit_message(request.json['key'], request.json['message'])
        return {
            "status": 200,
            "message": "edit message success !!!"
        }