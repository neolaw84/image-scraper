import numpy as np
import time

def delay_mean_and_std(mean:int = 5, std:int = 3):
    if not delay_mean_and_std.init:
        np.random.seed(delay_mean_and_std.seed)
        delay_mean_and_std.init = True
    time.sleep(np.random.normal(loc=mean, scale=std)/1.0)

delay_mean_and_std.seed=123456
delay_mean_and_std.init=False
