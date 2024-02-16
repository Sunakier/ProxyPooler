# -*- coding: utf-8 -*-
import re
from time import sleep

from model import daili
from ylib import *

__ipget__module__ = {
    "name": "开心代理",
    "ver": 1,
    "vername": "v1.0"
}


class dip(daili):
    name = "开心代理"

    def __init__(self, callback, num=10):
        super().__init__(callback, num)

    def main(self):
        url1 = "http://www.kxdaili.com/dailiip/1/"
        url2 = "http://www.kxdaili.com/dailiip/2/"

        def bkaixin(kurl, type):
            listx = []  # 一个类型的
            for i in range(self.num):
                url_2 = kurl + str(i + 1) + ".html"
                self.ylog("获取 " + type + " 第 " + str(i + 1) + " 页 K:" + str(i))
                text_2 = None
                self.session.headers.update({"Referer": url_2})  # 一定要带referer否则封ip
                for ix in range(5):
                    try:
                        rs = self.session.get(url=url_2, timeout=self.timeout)
                        if rs.status_code != 200:
                            self.ylog("获取 " + type + " 第 " + str(i + 1) + " 页 失败C:" + str(rs.status_code) + " T:" + str(ix))
                            sleep(1)
                            continue
                        text_2 = rs.text
                        break
                    except:
                        sleep(1)
                        self.ylog("获取 " + type + " 第 " + str(i + 1) + " 页 失败 T:" + str(ix))
                if text_2 is None:
                    self.ylog("获取 " + type + " 第 " + str(i + 1) + " 页 失败 重试次数过多")
                    continue

                text_4 = textGetMiddle(text_2, '''<table class="active">''', "</table>")
                text_5 = textGetMiddle(text_4, '''<tbody>''', "</tbody>")
                text_6 = textDelSpace(text_5)
                pattern = r'<tr(.*?)><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>'
                matchsx = re.findall(pattern, text_6)

                listz = []  # 一个页面的
                for match in matchsx:
                    ip = str(match[1]).strip() + ":" + str(match[2]).strip()
                    listz.append(ip)
                if len(listz) <= 0:  # 没了
                    break
                listx = listx + listz
                sleep(1)

            return list(set(listx))

        rs = list(set(bkaixin(url1, "高匿") + bkaixin(url2, "普匿")))  # 一整个任务的
        return {"http": rs}


if __name__ == '__main__':
    def callback():
        pass


    import json

    ax = dip(callback(), 2)
    h = ax.main()
    print(len(h['http']), "个", "\n" + json.dumps(h))
