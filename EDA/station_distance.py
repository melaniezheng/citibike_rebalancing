# Calculate each citibike station to each of all other citibike stations.
# Distance calculation: using Manhattan distance. Distance= Abs(lat1-lat2)+Abs(long1-long2)
# Format: Nested Dictionary. { station1: {station2: distance(station1,station2), station3: distance(station1,station3),...},
#                              station2: {station1: distance(station2,station1), station3: distance(station2,station3),...},
#                              station3: {...}, station4: {...}, station5:{...},...} 

import pandas as pd
import numpy as np
import time

# load stations
stations = pd.read_csv('../Data/live_stations.csv') # all stations after '2019-12-01'. There are 895 'live' stations.

station_dict={}
for station in stations.station_id.unique().tolist(): # loop through each station
    loc1=(stations[stations.station_id==station].station_lat.values,\
        stations[stations.station_id==station].station_long.values) # tuple (lat1, long1) 
    others=[x for x in stations.station_id.unique().tolist() if x != station] # list of each of all other stations

    dist_to_others={} # initiate empty dictionary. this is one of the inner dictionaries in the final nested distionary.
    for othr_station in others:
        loc2=(stations[stations.station_id==othr_station].station_lat.values,\
            stations[stations.station_id==othr_station].station_long.values) # tuple(lat2, long2)
        distance=(abs(loc1[0]-loc2[0])+abs(loc1[1]-loc2[1]))[0] # calculate manhattan distance
        dist_to_others[othr_station]=distance # store distance in dictionary

    dist_to_others=sorted(dist_to_others.items(), key = lambda kv:(kv[1], kv[0])) # sort stations by shortest distance to itself
    station_dict[station]=dist_to_others

import pickle
output = open('../Data/station_dict.pkl', 'wb')
pickle.dump(station_dict, output, -1)
output.close()