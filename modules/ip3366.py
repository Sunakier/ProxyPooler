from bs4 import BeautifulSoup
from urllib3 import disable_warnings

import ylib
from model import daili

__ipget__module__ = {
    "name": "IP3366",
    "ver": 1,
    "vername": "v1.0"
}


class dip(daili):
    name = "IP3366"

    def __init__(self, callback, num=10):
        super().__init__(callback, num)

    def main(self):

        surl = "http://www.ip3366.net/"
        headers = {
            "Host": "www.ip3366.net",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52",
            "Connection": "keep-alive"
        }
        disable_warnings()  # 关闭关闭证书校验的警告
        try:
            rs = self.session.get(url=surl, headers=headers, timeout=self.timeout)
        except Exception as error:  # 请求错误
            self.yerror(error, "GET HTML ERROR")
            return []
        rs.encoding = "utf-8"
        if rs.status_code != 200:
            self.yerror_m("GET HTML ERROR | C: " + str(rs.status_code) + " | RS:" + str(rs.text))
            return []
        try:
            soup = BeautifulSoup(rs.text, 'html.parser')
        except Exception as error:
            self.yerror(error, "LOAD HTML ERROR")
            return []

        table = soup.find('table')  # 找到包含代理信息的表格

        r2 = []

        for row in table.find_all('tr'):  # 遍历每一行
            cells = row.find_all('td')  # 找到每一行中的所有单元格
            if len(cells) == 8:  # 确保是代理信息行
                ip_address = cells[0].text  # 提取IP地址
                port = cells[1].text  # 提取端口
                if ip_address.find(".") != -1 and ylib.Dck(port):
                    r2.append(ip_address + ":" + port)

        rs = list(set(r2))
        return {"http": rs}


if __name__ == '__main__':
    def callback():
        pass


    import json

    ax = dip(callback())
    h = ax.main()
    print(json.dumps(h))
