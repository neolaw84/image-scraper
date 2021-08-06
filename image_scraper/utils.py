import numpy as np
import time

def delay_mean_and_std(mean:int = 5, std:int = 3):
    if not delay_mean_and_std.init:
        np.random.seed(delay_mean_and_std.seed)
        delay_mean_and_std.init = True
    time.sleep(np.random.normal(loc=mean, scale=std)/1.0)

delay_mean_and_std.seed=123456
delay_mean_and_std.init=False

def check_if_visited_and_add(url:str=None):
    if not check_if_visited_and_add.init:
        check_if_visited_and_add.urls = {}
        check_if_visited_and_add.init = True
    url_parts = url.split("/")
    urls = check_if_visited_and_add.urls
    for p in url_parts:
        if p in urls.keys():
            urls = urls[p]
        elif p == url_parts[-1]:
            urls[p] = True
            return False
        else:
            urls[p] = {}
            urls = urls[p]
    return True

check_if_visited_and_add.init=False
