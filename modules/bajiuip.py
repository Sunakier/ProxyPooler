from model import daili

__ipget__module__ = {
    "name": "89IP",
    "ver": 1,
    "vername": "v1.0"
}


class dip(daili):
    name = "89IP"

    def __init__(self, callback, num=2):
        super().__init__(callback, num)

    def main(self):
        from lxml.etree import HTML
        from time import sleep

        headers = {
            "Referer": "http://api.89ip.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42"
        }

        r2 = []

        for i in range(self.num):
            surl = "http://api.89ip.cn/tqdl.html?api=1&num=9999"
            try:
                rs = self.session.get(url=surl, headers=headers, timeout=self.timeout)
            except Exception as error:  # 请求错误
                self.yerror(error, "GET HTML ERROR")
                continue
            if rs.status_code != 200:
                self.yerror_m("GET HTML ERROR | C: " + str(rs.status_code) + " | RS:" + str(rs.text))
                continue
            dom = HTML(rs.text)
            r1 = dom.xpath("""/html/body/text()""")

            for i in range(len(list(r1))):
                r3 = "".join(str(list(r1)[i]).split())
                if r3 != "" and r3.find(":") != -1:
                    r3 = r3.split("@")[0]
                    r2.append(r3)
            sleep(0.4)

        rs = list(set(r2))

        return {"http": rs}
