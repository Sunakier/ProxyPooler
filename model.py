# -*- coding: utf-8 -*-
from ylib import *
from threading import Thread
from requests import session


class daili(Thread):
    def __init__(self, callback, num=10):
        self.num = num
        self.session = session()
        self.timeout = 10
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.33 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        }
        self.session.headers.update(headers)
        self.callback = callback
        Thread.__init__(self)

    def ylog(self, msg):
        print("[" + self.name + "] INFO " + str(milliSecondToTime(milliTime())) + " | " + str(msg))

    def yerror(self, error, msg=""):
        if isinstance(error, Exception):
            print("[" + self.name + "] ERROR " + str(milliSecondToTime(milliTime())) + " | M: " + str(__name__) + " | L: " + str(error.__traceback__.tb_lineno) + " | E:" + str(type(error.__traceback__.tb_frame.f_locals['error'])) + " | D: " + str(msg))
        try:
            self.yerror_m(str(error))
        except:
            pass

    def yerror_m(self, msg):
        print("[" + self.name + "] ERROR_M | M: " + str(__name__) + " | E:" + str(msg))

    def run(self):
        self.ylog("启动 获取页数: " + str(self.num))
        rs = self.main()
        self.callback(rs, self.name)
        # try:
        #     rs = self.main()
        #     self.callback(rs)
        # except Exception as error:
        #     self.yerror(error, "线程运行出现大错误, 请更新对应模块")

    def main(self):
        return []
