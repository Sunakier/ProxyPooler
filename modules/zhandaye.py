# -*- coding: utf-8 -*-
import re
from time import sleep

from urllib3 import disable_warnings

from model import daili

__ipget__module__ = {
    "name": "站大爷",
    "ver": 1,
    "vername": "v1.0"
}


class dip(daili):
    name = "站大爷"

    def __init__(self, callback, num=3):
        super().__init__(callback, num)

    def main(self, debug=False):
        disable_warnings()
        url_1 = "https://www.zdaye.com/dayProxy.html"
        headers = {
            "Host": "www.zdaye.com"
        }
        self.session.headers.update(headers)
        text_1 = None
        for i in range(5):
            try:
                rs = self.session.get(url=url_1, timeout=self.timeout)
                if rs.status_code == 405:
                    self.yerror_m("IP 不干净")
                    return {}
                if rs.status_code != 200:
                    self.yerror_m("获取主页失败 C:" + str(rs.status_code) + " T:" + str(i))
                    sleep(1)
                    continue
                text_1 = rs.text
                break
            except:
                sleep(1)
                self.yerror_m("获取主页失败 T:" + str(i))
        if text_1 is None:
            self.yerror_m("获取主页失败 重试次数过多")
            return {}

        text_1 = text_1.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
        pattern = r'<divclass="content"><divclass="arctitle"><ahref="/dayProxy/ip/(.*?).html">(.*?)</a></div><divclass="arccont"><ahref="/dayProxy/ip/(.*?).html"><divclass="shortCont">(.*?)</div></a></div><divclass="arcauther"><spanclass="zuozhe"><iclass="icon-user"></i>站大爷</span><spanclass="innergfp"><spanclass="innergf">官方</span></span><spanclass="wtime"><iclass="icon-clock"></i>(.*?)</span></div></div>'
        matchs = re.findall(pattern, text_1)

        self.ylog("获取到" + str(len(matchs)) + "页索引")
        if len(matchs) != 0:
            sleep(1)
            if len(matchs) > self.num:
                willGet = self.num
            else:
                willGet = len(matchs)
            listx = []
            for i in range(willGet):
                url_2 = "https://www.zdaye.com/dayProxy/ip/" + str(matchs[i][0]).strip() + ".html"
                self.ylog("获取页 " + str(matchs[i][0]) + " (" + str(matchs[i][4]) + ") K:" + str(i))
                text_2 = None
                for ix in range(5):
                    try:
                        rs = self.session.get(url=url_2, timeout=self.timeout)
                        if rs.status_code != 200:
                            if rs.status_code == 405:
                                self.yerror_m("IP 不干净")
                                return {"http": listx}
                            if rs.status_code == 500:
                                self.yerror_m("已黑IP")
                                return {"http": listx}
                            self.yerror_m("获取页 " + str(matchs[i][0]) + "(" + str(matchs[i][4]) + ") 失败C:" + str(rs.status_code) + " T:" + str(ix))
                            sleep(1)
                            continue
                        text_2 = rs.text
                        break
                    except:
                        sleep(1)
                        self.yerror_m("获取页 " + str(matchs[i][0]) + "(" + str(matchs[i][4]) + ") 失败 T:" + str(ix))
                if text_2 is None:
                    self.yerror_m("获取页 " + str(matchs[i][0]) + "(" + str(matchs[i][4]) + ") 失败 重试次数过多")
                    continue
                text_5 = '''<table id="ipc" style="margin-bottom:20px;">'''
                text_3 = text_2[text_2.find(text_5) + len(text_5):]
                text_4 = text_3[:text_3.find('''</table>''')]
                text_6 = text_4.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
                pattern = r'<tr><td>(.*?)</a></td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>'
                matchsx = re.findall(pattern, text_6)

                for match in matchsx:
                    ip = str(match[0]).strip() + ":" + str(match[1]).strip()
                    listx.append(ip)
            listx = list(set(listx))
            return {"http": listx}
        return {}
