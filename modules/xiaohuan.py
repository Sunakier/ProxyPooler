from bs4 import BeautifulSoup

from model import daili

__ipget__module__ = {
    "name": "小幻代理",
    "ver": 1,
    "vername": "v1.0"
}


class dip(daili):
    name = "小幻代理"

    def __init__(self, callback, num=10):
        super().__init__(callback, num)

    def main(self):
        import cloudscraper
        session = cloudscraper.create_scraper()

        headers = {
            "Referer": "https://ip.ihuan.me/ti.html",
            "Host": "ip.ihuan.me",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.42"
        }

        r2 = []

        for i in range(self.num):
            surl = "https://ip.ihuan.me/tqdl.html"
            try:
                rs = session.post(url=surl, headers=headers, params={"num": "1000", "port": "", "kill_port": "", "address": "", "kill_address": "", "anonymity": "", "type": "", "post": "", "sort": "", "key": "9d53df797313673ecd48ba9a9da895d8"}, timeout=self.timeout)
            except Exception as error:  # 请求错误
                self.yerror(error, "GET HTML ERROR")
                continue
            if rs.status_code == 403:
                self.yerror("遇非免费版CF三秒盾, 跳过")
                break
            if rs.status_code != 200:
                self.yerror_m("GET HTML ERROR | C: " + str(rs.status_code) + " | RS:" + str(rs.text))
                continue
            print(rs.text)
            soup = BeautifulSoup(rs.text, 'html.parser')
            soup = soup.find("div", class_="panel-body")
            print(soup)

        rs = list(set(r2))

        return {"http": rs}


if __name__ == '__main__':
    def callback():
        pass


    import json

    ax = dip(callback())
    h = ax.main()
    print(json.dumps(h))
