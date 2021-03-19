#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Short script to read in a log file from a Geobit digitizer and
plot out the voltages over time.  Useful for evaluating digitizer
performance and continuity of power.

Created on Thu Nov  8 16:54:54 2018

@author: timb
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')

#%%

digitizer = 'GB3'


#dirname = '/Users/timb/Desktop/GB5/CONTROL/'
dirname = '/Volumes/labdata/basic_data/seismic_data/RAW/MoVE/SV_201810/' 
logfilename = '/CONTROL/LOG.TXT'
posfilename = '/CONTROL/POS.TXT'

#%%

search_string = 'Power Supply Voltage <'

file_object  = open(dirname+digitizer+logfilename, 'rb')
strings = file_object.readlines()

pos_file  = open(dirname+digitizer+posfilename, 'rb')
pos_bytes = pos_file.readlines()
pos = pos_bytes[0].decode('utf-8')

if digitizer == 'GB5':
    station = 'SE57'
elif digitizer == 'GB2':
    station = 'SE50'
elif digitizer == 'GB3':
    station = 'SE60'
elif digitizer == 'GB1':
    station = 'SEHC'
    
#%%


data = pd.DataFrame(columns=['time', 'volt'])
data = data.append({'time': pd.Timestamp('2018-04-26'), 
                    'volt': 14.0}, 
                    ignore_index=True )

for i in np.arange(len(strings)):
    linestring = strings[i].decode('utf-8')
    ind = linestring.find(search_string) + len(search_string)
#    print(ind)
    if ind > 5 + len(search_string):
        time_str = linestring[0:17]
        pd_time = pd.to_datetime(time_str, format='%d/%m/%y %H:%M:%S')
        if pd_time < pd.Timestamp('2001-02-01'):
            pd_time = data['time'].iloc[-1] + pd.Timedelta('1 seconds')
            volt_str = '11000' #np.nan
#        times = np.append(times, 
#                           )
#        times = np.append(times, 
#                          pd.to_datetime(time_str, infer_datetime_format=True) )
        else:
            volt_str = linestring[ind : ind+5]
#        volt = float(volt_str) / 1000
#        print('Hello ' + str(i))
        data = data.append({'time': pd_time, 
                            'volt': float(volt_str) / 1000}, 
                            ignore_index=True )


#%%
fig, ax = plt.subplots(num = 1, clear=True)
ax.plot(data['time'], data['volt'], '-')
ax.set_title(station + ' (' + digitizer + ') '+ ', at location ' + pos)
ax.set_ylim(10.8, 15.3)
ax.set_ylabel('Volts')
ax.set_xlim(np.datetime64('2018-04-27'), np.datetime64('2018-08-23'))
fig.savefig('volts_' + station + '_' + digitizer + '.png', dpi=300)


