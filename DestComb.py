# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 16:53:40 2021

@author: andub
"""

import geopandas as gpd
import numpy as np

def kwikdist(origin, destination):
    """
    Quick and dirty dist [nm]
    In:
        lat/lon, lat/lon [deg]
    Out:
        dist [nm]
    """
    # We're getting these guys as strings
    lona = float(origin[0])
    lata = float(origin[1])

    lonb = float(destination[0])
    latb = float(destination[1])

    re      = 6371000.  # radius earth [m]
    dlat    = np.radians(latb - lata)
    dlon    = np.radians(((lonb - lona)+180)%360-180)
    cavelat = np.cos(np.radians(lata + latb) * 0.5)

    dangle  = np.sqrt(dlat * dlat + dlon * dlon * cavelat * cavelat)
    dist    = re * dangle
    return dist

origins = gpd.read_file('Sending_nodes.gpkg').to_numpy()[:,0:2].astype('float64')
destinations = gpd.read_file('Recieving_nodes.gpkg').to_numpy()[:,0:2].astype('float64')

pairs = []

for origin in origins:
    for destination in destinations:
        if kwikdist(origin, destination) >=800:
            pairs.append([origin, destination])

