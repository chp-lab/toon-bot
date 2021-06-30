from requests.api import head
from hooking import Hooking
from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module
from datetime import datetime
import urllib3
import json
from openpyxl import Workbook
from openpyxl.styles import Font, Fill
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
import os
from flask import stream_with_context, Response
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Export_excel(Resource):
    TAG = "ExportAsExcel:"
    file_path = "/home/user01/ibeacon-dev/tmp"
    # file_path = "./ibeacon-dev/tmp"
    # file_path = "/tmp"
    tmp_file_name = ""
    new_file_name = "default"

    def __init__(self):
        # clear file extension
        # file_name = args.get("file_name")
        self.file_path = self.file_path
        print(self.TAG, self.file_path, " Hereeeeeeeeeeee")
        if (not os.path.exists(self.file_path)):
            print(self.TAG, self.file_path, " Thissssssssssssssss")
            os.mkdir(self.file_path)
            # print(self.TAG, file_path, "dir created")
        # self.new_file_name = file_name.replace(".xlsx", "")
        filename = request.args['file_name']
        self.new_file_name = filename + ".xlsx"
        # create full path
        self.tmp_file_name = self.file_path + "/" + self.new_file_name
        print(self.tmp_file_name)

    # user who open file location

    def open_file_location(self):
        # print(self.TAG, "%s$Location:" %(user), self.tmp_file_name)
        return {"file_path": self.file_path, "file_name": self.new_file_name}

    # def read_file(self):
    #     print(self.TAG, "read file", self.tmp_file_name)
    def export_file(self, table):
        # print(self.TAG, "exportFile")
        wb = Workbook()
        # ws = wb.create_sheet(0)
        ws = wb.active
        # ws.title = "Sheet"
        # print(self.TAG, "Exporting to", self.tmp_file_name)
        for col in table["head"]:
            print(col)
        try:
            print(self.TAG, "heads=", table["head"])
            if (table["head"] is None):
                return False
            heads = ["No."] + table["head"]
            #             print(self.TAG, "heads=",heads)
            if ("reverse_cut" in table):
                print("reverse cut found")
                heads.pop()
            ws.append(heads)
            # for data in table["data"]:
            #     ws.append(data)
            for col_name in table:
                print(self.TAG, col_name)
            if (table["data"] is not None):
                data_export = table["data"]
                print(self.TAG, "data type=", type(table["data"]))
                if (isinstance(data_export, str)):
                    data_export = json.loads(data_export)
                cut_num = 0
                if ("cut" in table):
                    print("cut=", table["cut"])
                    num_col = 0
                    try:
                        cut_num = int(table["cut"])
                        if (len(data_export) > 0):
                            num_col = len(data_export[0])
                        if("reverse_cut" in table):
                            num_col = num_col - int(table["reverse_cut"])
                    except Exception as err2:
                        print(self.TAG, "DB0X01 error on cutting, err=", err2)
                        return False

                    for i in range(len(data_export)):
                        tmp_data = [i + 1] + data_export[i][cut_num:num_col]
                        ws.append(tmp_data)
                else:
                    for i in range(len(data_export)):
                        tmp_data = [i + 1] + data_export[i]
                        ws.append(tmp_data)

                if (("sum_at_table_footer_lbl" in table) and (len(data_export) > 0)):
                    num_col = len(data_export[0]) + 1 - cut_num
                    # add no col
                    if(num_col > 2):
                        blank_footer = []
                        for i in range(num_col - 2):
                            blank_footer.append("")
                    blank_footer.append(table["sum_at_table_footer_lbl"])
                    tmp_order_number = []
                    # fixed index
                    sum = 0
                    order_number_id = 8
                    status_id = 9
                    price_vat_id = 21
                    try:
                        order_number_id = order_number_id + cut_num - 1
                        status_id = status_id + cut_num - 1
                        price_vat_id = price_vat_id + cut_num - 1

                        for row in data_export:
                            # print("order_number=", row[order_number_id])
                            # print("status=", row[status_id])
                            # print("price=", row[price_vat_id])
                            if(row[order_number_id] not in tmp_order_number):
                                tmp_order_number.append(row[order_number_id])
                                # print("new order found!")
                                if(row[status_id] == "approved"):
                                    # print("approved")
                                    sum = sum + float(row[price_vat_id])
                    except Exception as err2:
                        print(self.TAG, "DB0X02 err=", err2)
                        # return False

                    print("sum=", sum)

                    blank_footer.append(sum)
                    ws.append(blank_footer)
            #                 for i in range(len(heads)):
            #                     ws.cell(1, i + 1).font = Font(bold=True)
            #                     ws.column_dimensions[chr(ord('A') + i)].width = 25
            # ws.column_dimensions[get_column_letter(i + 1)].width = 25

            # edit sheet style
            try:
                for i in range(len(heads)):
                    ws.cell(1, i + 1).font = Font(bold=True)
                    ws.column_dimensions[get_column_letter(i + 1)].width = 25
                    # get last row
                    ws.cell(len(data_export) + 2, i + 1).font = Font(bold=True)
            except Exception as err2:
                print(self.TAG, "DB0X03 err=", err2)
                return False

            wb.save(self.tmp_file_name)
        except Exception as err:
            print(self.TAG, "error on exporting excel")
            print(self.TAG, "DB0X04 err=", err)
            return False

        return True
    # def delete_file(self):
    #     print(self.TAG, "delete file", self.tmp_file_name)
    #     try:
    #         os.remove("demofile.txt")
    #     except Exception as err:
    #         print(self.TAG, "err=", err)

    # def edit_file(self, table):
    #     print(self.TAG, "edit file", self.tmp_file_name)

    def download_file(self, file_path, file_name):
        tmp_file_name = file_path + "/" + file_name
        print("DOWNLOAD ", tmp_file_name, " Thissssssssssssssss here")
        # if (not os.path.exists(self.file_path)):
        #     print(self.TAG, self.file_path, " Thissssssssssssssss")
        #     os.mkdir(self.file_path)
        # wb = Workbook(tmp_file_name)
        # wb.add_worksheet('All Data')

        # for item in values.fetchall():
        #     wb.write(item)
        # wb.close()
        # url = "http://203.151.164.229:5008/api/v1/report/export/" + tmp_file_name + ".xlsx"
        # print("URL : ", url)
        # r = requests.get(url, allow_redirects=True)
        # open(url, 'wb').write(r.content)
        # return "OK"

    def post(self):
        # args = request.args
        # excel_file = Export_excel(args)
        # excel_file = Export_excel(self.new_file_name)
        # excel_file = self.__init__(self, args)
        print("kkkkkkkkkkkkkkkkkkkkk")
        print(request.json)
        print("sssss", request.json['head'])
        print(request.json['data'])

        dataFile = {
            "head": request.json['head'],
            "data": request.json['data']
        }
        excel_file = self.export_file(dataFile)
        file_location = self.open_file_location()
        print("Location: ", file_location)

        return file_location

    def get(self):
        filename = request.args['file_name']
        filepath = request.args['file_path']
        # return Response(stream_with_context(self.download_file(filename, filepath)))
        return "OK"
