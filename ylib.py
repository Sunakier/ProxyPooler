def milliTime(time=None):
    if time is None:
        from time import time
        time = time()
    return int(round(time, 4) * 1000)


# 13位时间戳转换为日期格式字符串
def milliSecondToTime(millis):
    from time import strftime, localtime
    return strftime('%Y-%m-%d %H:%M:%S', localtime(millis / 1000))


# 自查
def Dck(a: str):
    try:
        a = str(a)
        if a == str(int(a)):
            return True
        else:
            return False
    except:
        return False


# 文本取中间 写法 未铺开
def textGetMiddle(text_all: str, text_1: str, text_2: str):
    text_3 = text_all[text_all.find(text_1) + len(text_1):]
    text_4 = text_3[:text_3.find(text_2)]
    return text_4


# 一键去空格回车换行缩进
def textDelSpace(text: str):
    return text.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
