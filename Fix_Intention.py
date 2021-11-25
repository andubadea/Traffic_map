# -*- coding: utf-8 -*-
import time
import random

def fix_times(df):
    for index, row in df.iterrows():
        # Get data
        start_time = text2time(row[3])
        if row[6] == 4:
            if start_time < 60:
                known_time = time2text(0)
            else:
                # Just subtract 60 seconds and done
                known_time = start_time - 60
            df.loc[index,0] = time2text(known_time)
    return df

def text2time(string_time):
    hours = int(string_time[0]+string_time[1])
    minutes = int(string_time[3] + string_time[4])
    seconds = int(string_time[6] + string_time[7])
    return hours*3600 + minutes * 60 + seconds

def time2text(time_s):
    return time.strftime('%H:%M:%S', time.gmtime(time_s))
