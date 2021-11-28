import time


def reserse(src):
    time.sleep(7)
    return src[::-1]


def change_letters(src):
    time.sleep(3)
    if len(src) < 2:
        return src
    len_src = len(src)
    if len_src % 2 != 0:
        len_src = len_src - 1
    s = ""
    for i in range(0, len_src - 1, 2):
        s = src[i] + src[i + 1]
    return s
