from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from booking import Booking
from check_perm import Check_perm
from hooking import Hooking
from qr_decode import Qr_decode
from my_mqtt import My_mqtt
from admin.get_timeattendance import Timeattendance
from admin.custommessage import Custommessage
from admin.get_Replymessage import Replymessage
from checkin_system_mockup.get_userprofile import Userprofile
from checkin_system_mockup.check_in import Check_in
from checkin_system_mockup.update_checkout import Check_out
from users import Users


# from monitor import Monitor
from covid_log import Covid_log


class Server:
    app = None
    api = None
    meter = None
    # monitor = None

    def __init__(self):
        print("init")
        self.app = Flask(__name__)
        CORS(self.app)
        self.api = Api(self.app)


if (__name__ == "__main__"):
    TAG = "main:"
    API_VERSION = "/api/v1"
    server = Server()
    # monitor = Monitor()
    # my_mqtt = My_mqtt()

    # server.api.add_resource(Check_perm, API_VERSION + "/check_perm/<room_num>")
    # server.api.add_resource(Booking, API_VERSION + "/booking/<booking_number>")
    server.api.add_resource(Hooking, API_VERSION + "/hooking")
    # server.api.add_resource(Qr_decode, API_VERSION + "/myqr")
    # server.api.add_resource(My_mqtt, API_VERSION + "/unlock/<room_num>")
    server.api.add_resource(Covid_log, API_VERSION + "/covid/log")
    server.api.add_resource(
        Timeattendance, API_VERSION + "/admin/get_timeattendance")
    server.api.add_resource(
        Custommessage, API_VERSION + "/admin/custommessage")
    server.api.add_resource(Replymessage, API_VERSION +
                            "/admin/get_replymessage")
    server.api.add_resource(Userprofile, API_VERSION + "/get_userprofile")
    server.api.add_resource(Check_in, API_VERSION + "/check_in")
    server.api.add_resource(Check_out, API_VERSION + "/check_out")
    server.api.add_resource(Users, API_VERSION + "/profile")
    server.app.run(host="0.0.0.0", debug=True, port=5008)
