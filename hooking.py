# -- coding: utf-8 --

from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module

class Hooking(Resource):
    onechat_uri = "https://chat-api.one.th"
    onechat_dev_token = "Bearer A75817cf7dfd75dbabbc72a05dcabc48dd461161461394afb914f5e3a06eb7d0201f0e90d89534e56949dc870e0e54618"
    onechat_url1 = onechat_uri + '/message/api/v1/push_quickreply'
    def menu_send(self, user_id, bot_id):
        TAG = "menu_send:"
        # web_vue_url1 = "https://web-meeting-room.herokuapp.com/"
        web_vue_url1 = "https://onesmartaccess.herokuapp.com/"
        req_body = {
            "to": user_id,
            "bot_id": bot_id,
            "message": "อยากทราบเรื่องอะไรคะ?",
            "quick_reply":
                [
                    {
                        "label": "นิสัยตามกรุ๊ปเลือด",
                        "type": "text",
                        "message": "นิสัยตามกรุ๊ปเลือด",
                        "payload": {"action": "blood_type"}
                    },
                    # {
                    #     "label": "ทำความรู้จักผู้คน",
                    #     "type": "text",
                    #     "message": "มีใครโสดอยู่บ้าง",
                    #     "payload": {"action": "find_single"}
                    # },
                    {
                        "label": "อัพเดทโปรไฟล์",
                        "type": "text",
                        "message": "อัพเดทโปรไฟล์",
                        "payload": {"action": "profile_update"}
                    }
                ]
        }
        headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
        result = requests.post(self.onechat_url1, json=req_body, headers=headers)
        print(TAG, result.text)
    def send_msg(self, one_id, reply_msg):
        TAG = "send_msg:"
        bot_id = "Bab44da092865594fb367ff3933461af1"
        headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
        payload = {
            "to": one_id,
            "bot_id": bot_id,
            "type": "text",
            "message": reply_msg,
            "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
        }
        r = requests.post(self.onechat_uri + "/message/api/v1/push_message", headers=headers, json=payload)
        # self.menu_send(one_id, bot_id)
        return r

    def is_user_exist(self, one_email):
        TAG = "is_user_exist:"
        cmd = """SELECT users.one_email FROM users WHERE users.one_email='%s' """ %(one_email)
        database = Database()
        res = database.getData(cmd)
        print(TAG, "res=", res)
        if(res[0]['len'] > 0):
            return True
        else:
            return False

    def add_new_user(self, email, name, one_id):
        TAG = "add_new_user:"
        database = Database()
        print(TAG, "add user to our system")
        sql = """INSERT INTO `users` (`one_email`, `one_id`, `name`, `role`, `gender`, `age`, `created_at`) 
        VALUES ('%s', '%s', '%s', NULL, NULL, NULL, CURRENT_TIMESTAMP)""" % (email, name, one_id)
        insert = database.insertData(sql)
        return insert

    def update_data(self, cmd):
        TAG = "update_data"
        database = Database()
        print(TAG, "update=", cmd)
        update = database.insertData(cmd)
        return update

    def delete_data(self, cmd):
        TAG = "delete_data"
        database = Database()
        delete = database.insertData(cmd)
        print(TAG, "delete=", delete)
        return delete
    def send_quick_reply(self, one_id, req_body):
        TAG = "quick_reply"
        headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
        result = requests.post(self.onechat_url1, json=req_body, headers=headers)
        print(TAG, result.text)

    def gender_quest(self, user_id, bot_id):
        this_quest = {
                        "to": user_id,
                        "bot_id": bot_id,
                        "message": "คุณเพศอะไร",
                        "quick_reply":
                            [
                                {
                                    "label": "ชาย",
                                    "type": "text",
                                    "message": "ผู้ชายครับ",
                                    "payload": {"gender": "man"}
                                },
                                {
                                    "label": "หญิง",
                                    "type": "text",
                                    "message": "ผู้หญิงค่ะ",
                                    "payload": {"gender": "woman"}
                                },
                                {
                                    "label": "ไม่ระบุ",
                                    "type": "text",
                                    "message": "ไม่ระบุ",
                                    "payload": {"gender": "not_specified"}
                                }
                            ]
                    }
        return this_quest

    def blood_data(self, user_id, bot_id):
        this_quest = {
                        "to": user_id,
                        "bot_id": bot_id,
                        "message": "คุณกรุ๊ปเลือดอะไร?",
                        "quick_reply":
                            [
                                {
                                    "label": "A",
                                    "type": "text",
                                    "message": "A",
                                    "payload": {"blood_data": "A"}
                                },
                                {
                                    "label": "O",
                                    "type": "text",
                                    "message": "O",
                                    "payload": {"blood_data": "O"}
                                },
                                {
                                    "label": "B",
                                    "type": "text",
                                    "message": "B",
                                    "payload": {"blood_data": "B"}
                                },
                                {
                                    "label": "AB",
                                    "type": "text",
                                    "message": "AB",
                                    "payload": {"blood_data": "AB"}
                                }
                            ]
                    }
        return this_quest

    def data_valid_quest(self, user_id, bot_id):
        this_quest = {
            "to": user_id,
            "bot_id": bot_id,
            "message": "ยืนยันข้อมูล",
            "quick_reply":
                [
                    {
                        "label": "ถูกต้อง",
                        "type": "text",
                        "message": "ข้อมูลถูกต้อง",
                        "payload": {"profile_confirm": "confirm"}
                    },
                    {
                        "label": "ไม่ถูกต้อง",
                        "type": "text",
                        "message": "ข้อมูลไม่ถูกต้อง",
                        "payload": {"profile_confirm": "eject"}
                    }
                ]
        }

        return this_quest

    def show_profile_data(self, user_id, bot_id):
        this_quest = {
            "to": user_id,
            "bot_id": bot_id,
            "message": "ยืนยันข้อมูล",
            "quick_reply":
                [
                    {
                        "label": "ถูกต้อง",
                        "type": "text",
                        "message": "ข้อมูลถูกต้อง",
                        "payload": {"profile_confirm": "confirm"}
                    },
                    {
                        "label": "ไม่ถูกต้อง",
                        "type": "text",
                        "message": "ข้อมูลไม่ถูกต้อง",
                        "payload": {"profile_confirm": "eject"}
                    }
                ]
        }
        return this_quest

    def select_data(self, user_id, bot_id):
        this_quest = {
            "to": user_id,
            "bot_id": bot_id,
            "message": "กรุณาเลือกสีที่ชอบ",
            "quick_reply":
                [
                    {
                        "label": "สีชมพู",
                        "type": "text",
                        "message": "สีชมพู",
                        "payload": {"select_color": "pink"}
                    },
                    {
                        "label": "สีเขียว",
                        "type": "text",
                        "message": "สีเขียว",
                        "payload": {"select_color": "green"}
                    }
                ]
        }
        return this_quest

    # core api
    def post(self):
        TAG = "Hooking:"

        database = Database()
        module = Module()
        # onechat_uri = self.onechat_uri

        # onechat_dev_token = "Bearer Af58c5450f3b45c71a97bc51c05373ecefabc49bd2cd94f3c88d5b844813e69a17e26a828c2b64ef889ef0c10e2aee347"
        # headers = {"Authorization": onechat_dev_token}

        data = request.json
        print(TAG, "data=", data)
        print(TAG, request.headers)

        if('event' not in data):
            print(TAG, "event not found!")
            # assum OneChat iBeacon event detected
            print(TAG, "my custom data")
            return module.success()
            # return module.wrongAPImsg()

        if(data['event'] != "message"):
            print(TAG, "event not support")
            return module.wrongAPImsg()

        bot_id = data['bot_id']
        user_id = data['source']['user_id']
        email = data['source']['email']
        one_id = data['source']['one_id']
        name = data['source']['display_name']

        print(TAG, "user_id=", user_id)
        print(TAG, "one email=", email)

        user_exist = self.is_user_exist(email)

        if(user_exist):
            print(TAG, "user already exist")
            msg_type = data["message"]["type"]
            print(TAG, "msg=",msg_type)

            # quick reply
            if ('data' in data['message']):
                if ("gender" in data['message']['data']):
                    gender = data['message']['data']["gender"]
                    print(TAG, "gen=", gender)
                    cmd = """UPDATE `users` SET `gender` = '%s' WHERE `users`.`one_email` = '%s'""" % (gender, email)
                    update = self.update_data(cmd)
                    print("gen update=", update)
                # elif("birt_date" in data['message']['data']):
                #     print(TAG, "record bd")
                    # send birth date question

            elif(msg_type == "text"):
                self.send_msg(one_id, "น้องดวงดี สวัสดีค่ะ :)")
                cmd = """SELECT users.name, users.gender , users.age FROM `users` WHERE users.one_email='%s'""" % (email)
                res = database.getData(cmd)
                print(TAG, "res=", res)

                gender = res[0]['result'][0]['gender']
                age = res[0]['result'][0]['age']

                # if (gender is None):
                #     req_body = self.gender_quest(user_id, bot_id)
                #     self.send_quick_reply(one_id, req_body)
                #     # return module.success()
                # elif(res[0]['result'][0]['age'] is None):
                #     self.send_msg(one_id, "คุณอายุเท่าไหร่?")
                #     age = data['message']['text']
                #     age = int(age)
                #     cmd = """UPDATE `users` SET `age` = '%s' WHERE `users`.`one_email` = '%s'""" %(age, email)
                #     update = self.update_data(cmd)
                #     print("age update=", update)
                if(gender is None or age is None):
                    req_body = self.gender_quest(user_id, bot_id)
                    # self.send_quick_reply(one_id, req_body)
                    self.send_msg(one_id, "คุณอายุเท่าไหร่?")
                    age = data['message']['text']
                    age = int(age)
                    cmd = """UPDATE `users` SET `age` = '%s' WHERE `users`.`one_email` = '%s'""" % (age, email)
                    update = self.update_data(cmd)
                    self.send_quick_reply(one_id, req_body)
                    print("age update=", update)


            else:
                print(TAG, "message not support!")
        else:
            print(TAG, "usr not exist!")
            add_user = self.add_new_user(email, name, one_id)
            print(TAG, "add=new_user=", add_user)
            self.send_msg(one_id, "น้องดวงดี สวัสดีค่ะ :)")
            req_body = self.gender_quest(user_id, bot_id)
            self.send_quick_reply(one_id, req_body)

        # if (user_exist):
        #     print(TAG, "### user exist!")
        #     if ('data' in data['message']):
        #         if ("gen" in data['message']['data']):
        #             gen = data['message']['data']["gen"]
        #             print(TAG, "gen=", gen)
        #             cmd = """UPDATE `users` SET `gender` = '%s' WHERE `users`.`one_email` = '%s'""" % (gen, email)
        #             update = self.update_data(cmd)
        #             print("gen update=", update)
        #             self.send_msg(one_id, "อายุเท่าไหร่คะ")
        #         elif ("interested_gen" in data['message']['data']):
        #             interested_gen = data['message']['data']['interested_gen']
        #             print(TAG, "interested_gen=", interested_gen)
        #             cmd = """UPDATE `users` SET `interested_in` = '%s' WHERE `users`.`one_email` = '%s'""" % (
        #             interested_gen, email)
        #             update = self.update_data(cmd)
        #             print(TAG, "interested_gen_update=", update)
        #             req_body = self.show_profile_data(user_id, bot_id)
        #             self.send_quick_reply(one_id, req_body)
        #         elif ("profile_confirm" in data['message']['data']):
        #             profile_confirm = data['message']['data']['profile_confirm']
        #             if (profile_confirm == "confirm"):
        #                 update = """UPDATE `users` SET `data_valid` = '%s' WHERE `users`.`one_email` = '%s'""" % (
        #                 True, email)
        #                 res = database.insertData(update)
        #                 print(TAG, "profile confirm=", res)
        #                 self.send_msg(one_id, "ผู้คนยินดีที่รู้จักคุณ")
        #                 self.menu_send(user_id, bot_id)
        #                 return module.success()
        #             elif (profile_confirm == "eject"):
        #                 print(TAG, "delete record")
        #                 cmd = """DELETE FROM `users` WHERE users.one_email='%s'""" % (email)
        #                 res = database.insertData(cmd)
        #                 print(TAG, "delete data=", res)
        #                 self.send_msg(one_id, "ไว้คุยกันใหม่นะ")
        #                 return module.unauthorized()
        #         elif ("action" in data['message']['data']):
        #             action = data['message']['data']['action']
        #             if (action == "find_single"):
        #                 self.send_msg(one_id, "พบกันเร็วๆ นี้ค่ะ")
        #                 return module.success()
        #             elif (action == "image_rec"):
        #                 self.send_msg(one_id, "ส่งรูปของคุณมาได้เลย")
        #                 return module.success()
        #         else:
        #             print(TAG, "unnown message data in quick reply")
        #     elif('type' in data['message']):
        #         msg_type = data['message']["type"]
        #         print(TAG, "msg_type=", msg_type)
        #         if (msg_type == "image"):
        #             self.send_msg(one_id, "กำลังพัฒนาระบบบันทึกรูป")
        #             return module.success()
        #         elif (msg_type == "text"):
        #             cmd = """SELECT users.age FROM users WHERE users.one_email='%s'""" % (email)
        #             res = database.getData(cmd)
        #             print(TAG, "check_age_dat=", res)
        #             if (res[0]['result'][0]['age'] is None):
        #                 age = data['message']['text']
        #
        #                 if (not age.isnumeric()):
        #                     self.send_msg(one_id, "อายุเท่าไหร่คะ กระรุณาระบุเป็นตัวเลขค่ะ")
        #                     return module.wrongAPImsg()
        #
        #                 age = int(age)
        #
        #                 if (age == 0):
        #                     self.send_msg(one_id, "อายุเท่าไหร่คะ กระรุณาระบุเป็นตัวเลขที่ถูกต้องค่ะ")
        #                     return module.wrongAPImsg()
        #                 print(TAG, "age=", age)
        #
        #                 if (age < 18 or age > 100):
        #                     self.send_msg(one_id, "อายุของคุณไม่อยู่ในช่วงที่กำหนด")
        #                     return module.unauthorized()
        #                 cmd = """UPDATE `users` SET `age` = '%s' WHERE `users`.`one_email` = '%s'""" % (age, email)
        #                 update = self.update_data(cmd)
        #                 print(TAG, "update=", update)
        #                 if (update[1] == 200):
        #                     print(TAG, "set age")
        #                     return module.success()
        #                 else:
        #                     self.send_msg(one_id, "อายุเท่าไหร่คะ ระบุเป็นตัวเลข")
        #                     module.success()
        #             else:
        #                 print("age valid")
        #                 self.menu_send(user_id, bot_id)
        #                 print(TAG, "menu sending")
        #         else:
        #             self.send_msg(one_id, "ยังไม่รองรับข้อความประเภท " + msg_type)
        #             return module.success()
        #     else:
        #         cmd = """SELECT users.name, users.gender, users.age, users.interested_in , users.data_valid
        #         FROM users WHERE users.one_email='%s'""" % (email)
        #
        #         res = database.getData(cmd)
        #
        #         if(res[1] == 200):
        #             tmp_data = res[0]['result'][0]
        #             if(tmp_data['gender'] is None):
        #                 req_body = self.gender_quest(user_id, bot_id)
        #                 self.send_quick_reply(one_id, req_body)
        #                 return module.success()
        #             elif(tmp_data['age'] is None):
        #                 print(TAG, "ask age")
        #                 self.send_msg(one_id, "อายุเท่าไหร่")
        #                 return module.success()
        #             elif(tmp_data['interested_in'] is None):
        #                 print(TAG, "ask interested_in")
        #                 req_body = self.interested_quest(user_id, bot_id)
        #                 self.send_quick_reply(one_id, req_body)
        #                 return module.success()
        #             elif(tmp_data['data_valid'] is None):
        #                 print(TAG, "profile not confirm")
        #                 tmp_msg = "ยินดีที่ได้รู้จักคุณ %s อายุ %s สนใจใน %s ยืนยันข้อมูลถูกต้อง" %(tmp_data['name'], tmp_data['age'], tmp_data['interested_in'])
        #                 self.send_msg(one_id, tmp_msg)
        #                 req_body = self.data_valid_quest(user_id, bot_id)
        #                 self.send_quick_reply(one_id, req_body)
        #                 return module.success()
        #             else:
        #                 print(TAG, "user data valid")
        #         else:
        #             print(TAG, "fail on check user data_valid")
        #             return module.serveErrMsg()
        # #first meet
        # else:
        #     print(TAG, "usr not exist!")
        #     self.send_msg(one_id, "สวัสดีค่ะ แนะนำตัวเองเเบื้องต้นพื่อหาผู้คนที่คุณสนใจ")
        #     req_body = self.gender_quest(user_id, bot_id)
        #     self.send_quick_reply(one_id, req_body)
        #     add_user = self.add_new_user(email, name, one_id)
        #     print(TAG, "add=new_user=", add_user)
        #
        #     return module.success()


        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
