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
    def post(self):
        print(type(request.json))
        print(request.json)
        return {
            "status": 200
        }