from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Replymessage(Resource):
    def get_replymessage(self, key):
        cmd = """SELECT message FROM bot_message WHERE bot_message.message_keys='%d'""" %(key)
        database = Database()
        res = database.getData(cmd)
        return res

    def post(self):
        reply_message = self.get_replymessage(request.json['key'])
        return reply_message
