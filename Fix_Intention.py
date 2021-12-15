# -*- coding: utf-8 -*-
import time
import numpy as np

def fix_times(df):
    rmindex = []
    for index, row in df.iterrows():
        print(index)
        # Get data
        start_time = text2time(row[3])
        if row[6] == 4:
            if start_time < 60:
                known_time = 0
            else:
                # Just subtract 60 seconds and done
                known_time = start_time - 60
            df.loc[index,0] = time2text(known_time)
        # We check distances cuz some origins and destinations are too close to 
        # each other
        dist = kwikdist(row[4], row[5])
        if dist < 800:
            rmindex.append(index)
    df.drop(rmindex, inplace = True)
    # Rearrange the df
    df = df.sort_values(by=3)
    df[1] = [f'D{x+1}' for x in range(len(df[1]))]
    return df

def text2time(string_time):
    hours = int(string_time[0]+string_time[1])
    minutes = int(string_time[3] + string_time[4])
    seconds = int(string_time[6] + string_time[7])
    return hours*3600 + minutes * 60 + seconds

def time2text(time_s):
    return time.strftime('%H:%M:%S', time.gmtime(time_s))

def kwikdist(origin, destination):
    """
    Quick and dirty dist [nm]
    In:
        lat/lon, lat/lon [deg]
    Out:
        dist [nm]
    """
    # We're getting these guys as strings
    origin = origin.replace('(','').replace(')','').split(',')
    lona = float(origin[0])
    lata = float(origin[1])
    
    destination = destination.replace('(','').replace(')','').split(',')
    lonb = float(destination[0])
    latb = float(destination[1])

    re      = 6371000.  # radius earth [m]
    dlat    = np.radians(latb - lata)
    dlon    = np.radians(((lonb - lona)+180)%360-180)
    cavelat = np.cos(np.radians(lata + latb) * 0.5)

    dangle  = np.sqrt(dlat * dlat + dlon * dlon * cavelat * cavelat)
    dist    = re * dangle
    return dist
