# -*- coding: utf-8 -*-

import re
from time import sleep

from urllib3 import disable_warnings

from model import daili

__ipget__module__ = {
    "name": "快代理",
    "ver": 1,
    "vername": "v1.0"
}


class dip(daili):
    name = "快代理"

    def __init__(self, callback, num=40):
        super().__init__(callback, num)

    def main(self, debug=False):
        disable_warnings()
        url_1 = "https://www.kuaidaili.com/free/inha/"  # 国内高匿开放
        url_2 = "https://www.kuaidaili.com/free/intr/"  # 国内普通开放
        url_3 = "https://www.kuaidaili.com/free/fps/"  # 海外
        listx = []

        def get_ips_k(url, type):
            listv = []
            for i_num in range(self.num):
                self.ylog("获取 " + type + " 第 " + str(i_num + 1) + " 页")
                urlx = url + str(i_num + 1) + "/"
                text_2 = None
                for ix in range(5):
                    try:
                        rs = self.session.get(url=urlx, timeout=self.timeout)
                        if rs.status_code != 200:
                            self.yerror_m("获取 " + type + " 失败 C:" + str(rs.status_code) + " T:" + str(ix))
                            sleep(0.3)
                            continue
                        text_2 = rs.text
                        break
                    except:
                        sleep(0.3)
                        self.yerror_m("获取 " + type + " 失败 T:" + str(ix))
                if text_2 is None:
                    self.yerror_m("获取 " + type + " 失败 重试次数过多")
                    continue
                text_5 = '''<table class="table table-b table-bordered table-striped">'''
                text_3 = text_2[text_2.find(text_5) + len(text_5):]
                text_4 = text_3[:text_3.find('''</table>''')]
                text_6 = text_4.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                pattern = r'<tr><tddata-title="IP">(.*?)</td><tddata-title="PORT">(.*?)</td><tddata-title="匿名度">(.*?)</td><tddata-title="类型">(.*?)</td><tddata-title="位置">(.*?)</td><tddata-title="(.*?)>(.*?)</td><tddata-title="最后验证时间">(.*?)</td><tddata-title="付费方式">(.*?)</td></tr>'
                matchsx = re.findall(pattern, text_6)

                for match in matchsx:
                    ip = str(match[0]).strip() + ":" + str(match[1]).strip()
                    listv.append(ip)
                    listx.append(ip)
                sleep(0.3)
            self.ylog("获取 " + type + " " + str(len(listv)) + " 个")

        get_ips_k(url_1, "国内高匿开放")
        get_ips_k(url_2, "国内普通开放")
        get_ips_k(url_3, "海外")

        listx = list(set(listx))
        return {"http": listx}
