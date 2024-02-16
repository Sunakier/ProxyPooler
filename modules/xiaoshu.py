# -*- coding: utf-8 -*-
from time import sleep

from lxml.etree import HTML

from model import daili

__ipget__module__ = {
    "name": "小舒代理",
    "ver": 1,
    "vername": "v1.0"
}


class dip(daili):
    name = "小舒代理"

    def __init__(self, callback, num=10):
        super().__init__(callback, num)

    def main(self):
        surl = "https://www.xsdaili.cn/"
        headers = {"Referer": "https://www.xsdaili.cn/"}
        self.session.headers.update(headers)
        try:
            rs = self.session.get(url=surl, headers=headers, timeout=self.timeout)  # 获取主列表
        except Exception as error:  # 请求错误
            self.yerror(error, "GET HTML ERROR")
            return {}
        rs.encoding = "utf-8"
        if rs.status_code != 200:
            self.yerror_m("GET HTML ERROR | C: " + str(rs.status_code) + " | RS:" + str(rs.text))
            return {}

        try:
            dom = HTML(rs.text)
            r1 = dom.xpath("""/html/body/div[5]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/a/@href""")
            if len(r1) >= 1:
                timesitpe = int(str(r1[0][13:]).split(".")[0])
            else:
                self.yerror("LOAD HTML ERROR")
                return {}
        except Exception as error:
            self.yerror(error, "LOAD HTML ERROR")
            return {}
        url1 = "https://www.xsdaili.cn/dayProxy/ip/"
        url2 = ".html"

        r2 = []

        for iv in range(self.num):
            url = url1 + str(timesitpe - iv) + url2
            try:
                rs = self.session.get(url=url)
            except Exception as error:  # 请求错误
                self.yerror(error, "GET HTML ERROR")
                continue
            rs.encoding = "utf-8"
            if rs.status_code != 200:
                self.yerror_m("GET HTML ERROR | C: " + str(rs.status_code) + " | RS:" + str(rs.text))
                continue
            try:
                dom = HTML(rs.text)
                xpath = """/html/body/div[5]/div/div[2]/div/div/div/div[2]/div/div[2]/div[2]/text()"""
                r1 = dom.xpath(xpath)
            except Exception as error:
                self.yerror(error, "LOAD HTML ERROR")
                continue

            for i in range(len(list(r1))):
                r3 = "".join(str(list(r1)[i]).split())
                if r3 != "" and r3.find(":") != -1:
                    r3 = r3.split("@")[0]
                    r2.append(r3)
            sleep(1)

        rs = list(set(r2))
        return {"http": rs}
