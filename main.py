# -*- coding: utf-8 -*-
import threading
import json
from ylib import *
from time import sleep
from os import listdir
from hashlib import md5
from sys import stdout

ydata = {
    "data": {
        "http": [],
        "socks4": [],
        "socks5": []
    },
    "ok": 0,
    "all": 0,
}

lock = threading.Lock()


def callback(pdata, name="未知"):
    global ydata
    with lock:
        __http = pdata.get("http")
        __socks4 = pdata.get("socks4")
        __socks5 = pdata.get("socks5")
        msg = ""
        if __http:
            ydata['data']['http'] = ydata['data']['http'] + __http
            msg = " HTTP:" + str(len(__http))
        if __socks4:
            ydata['data']['socks4'] = ydata['data']['socks4'] + __socks4
            msg = msg + " SOCKS4:" + str(len(__socks4))
        if __socks5:
            ydata['data']['socks5'] = ydata['data']['socks5'] + __socks5
            msg = msg + " SOCKS5:" + str(len(__socks5))
        ydata['ok'] = ydata['ok'] + 1
        if msg == "":
            print("[" + name + "] 完成 未获得代理")
        else:
            print("[" + name + "] 完成 获得数量:" + msg)
    stdout.write("完成进度: [{:<50}] {:.2f}%\n".format('=' * int(ydata['ok'] / ydata['all'] * 50), ydata['ok'] / ydata['all'] * 100))
    stdout.flush()


threads = []  # 线程池

print("[主线程] 开始加载模块")

modules = listdir("./modules")  # 模块目录
for module in modules:
    try:
        name = module.rsplit(".", 1)
        name_q = name[0]
        name_p = name[1]
        if name_p == "py":
            module = name_q
        else:
            continue
        if textDelSpace(module) != module:  # 模块名不允许空格换行和缩进
            continue
        ban_name = ["__init__", ""]
        if module in ban_name:
            continue
        mid = md5(module.encode("utf8")).hexdigest()
        exec("from modules." + module + " import __ipget__module__ as _" + mid)
        exec("from modules." + module + " import dip as m_" + mid)
        exec("__ver = int(_" + mid + "['ver'])")
        exec("__vername = textDelSpace(str(_" + mid + "['vername']))")
        exec("__name = textDelSpace(str(_" + mid + "['name']))")
        exec(f'''t = m_{mid}(callback, 1)''')
        exec("threads.append(t)")
        exec('''print("[模块] 加载模块 " + __name + " ( " + module + " ID: " + mid + " ) " + __vername + " (" + str(__ver) + ") 成功!")''')
    except Exception as error:
        # print(str(error.__traceback__.tb_lineno) + " | E:" + str(error))
        pass

ydata['all'] = len(threads)
print("[主线程] 加载模块完成 开始启动")
for thread in threads:
    thread.start()
    sleep(0.1)
print("[主线程] 启动完成")

# 等待所有线程完成
for t in threads:
    t.join()

print("[主线程] 任务完成 等待写入文件")

_http = list(set(ydata['data']['http']))
_socks4 = list(set(ydata['data']['socks4']))
_socks5 = list(set(ydata['data']['socks5']))

_http_json = json.dumps(_http)  # json
with open("./output/http.json", "w") as f:
    f.write(_http_json)
_socks4_json = json.dumps(_socks4)
with open("./output/socks4.json", "w") as f:
    f.write(_socks4_json)
_socks5_json = json.dumps(_socks5)
with open("./output/socks5.json", "w") as f:
    f.write(_socks5_json)

_http_text = ""  # text
for _s in _http:
    _http_text += _s + "\n"
with open("./output/http.txt", "w") as f:
    f.write(_http_text)
_socks4_text = ""
for _s in _http:
    _socks4_text += _s + "\n"
with open("./output/socks4.txt", "w") as f:
    f.write(_socks4_text)
_socks5_text = ""
for _s in _http:
    _socks5_text += _s + "\n"
with open("./output/socks5.txt", "w") as f:
    f.write(_socks5_text)


print("[主线程] 写入完成")
print("[主线程] 结果: HTTP:" + str(len(_http)) + " SOCKS4:" + str(len(_socks4)) + " SOCKS5:" + str(len(_socks5)))
