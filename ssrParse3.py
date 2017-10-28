#!usr/bin/python3.6
# -*- coding=utf-8 -*-
import requests
import base64

class ssrParse:
    def __init__(self):
        self.__server = ""
        self.__port = 443
        self.__password = ""
        self.__method = ""
        self.__protocol = ""
        self.__protocolparam = ""
        self.__obfs = ""
        self.__obfsparam = ""
        self.__remarks_base64 = ""
        self.__remarks = ""
        self.__group = ""

    # data ssr://aGstNS5taXRzd···
    def decode(self, data):
        data = data[6:]
        result = self.__ssrBase64decode(data)
        if len(result) > 0:
            dataPart = result.split("/?")
            self.__decodeOnePart(dataPart[0])
            self.__decodeTwoPart(dataPart[1])

    def format(self):
        dict = {}
        dict["remarks"] = self.__remarks
        dict["server"] = self.__server
        dict["server_port"] = self.__port
        dict["password"] = self.__password
        dict["method"] = self.__method
        dict["protocol"] = self.__protocol
        dict["protocolparam"] = self.__protocolparam
        dict["obfs"] = self.__obfs
        dict["obfsparam"] = self.__obfsparam
        dict["remarks_base64"] = self.__remarks_base64
        dict["group"] = self.__group
        return dict

    @staticmethod
    def base64decode(data, altchars=None):
        lens = len(data)
        fillNum = 4 - (lens % 4)
        data += "=" * fillNum
        try:
            result = base64.b64decode(data, altchars)
            return result
        except Exception as err:
            print("base64decode dataError\n" + data + "\n" + err)
            return ""

    @staticmethod
    def parseSubscribe(subscribeLink):
        try:
            content = requests.get(subscribeLink).text
            ssr = ssrParse.base64decode(content).decode("utf-8")
            return ssr.split("\n")
        except Exception as err:
            print(err)
            return ""

    def __decodeOnePart(self, onePart):  # 解析主要参数
        split = onePart.split(":")
        self.__server = split[0]
        self.__port = split[1]
        self.__protocol = split[2]
        self.__method = split[3]
        self.__obfs = split[4]
        self.__password = self.__ssrBase64decode(split[5])

    def __decodeTwoPart(self, twoPart):
        split = twoPart.split("&")
        for item in split:
            oneArg = item.split("=")
            if oneArg[0] == "obfsparam":
                self.__obfsparam = self.__ssrBase64decode(oneArg[1])
                continue
            if oneArg[0] == "protoparam":
                self.__protocolparam = self.__ssrBase64decode(oneArg[1])
                continue
            if oneArg[0] == "remarks":
                self.__remarks_base64 = oneArg[1]
                self.__remarks = self.__ssrBase64decode(oneArg[1])
                continue
            if oneArg[0] == "group":
                self.__group = self.__ssrBase64decode(oneArg[1])
                continue

    def __ssrBase64decode(self, str):
        altchars = "-_"
        return self.base64decode(str, altchars).decode("utf-8")