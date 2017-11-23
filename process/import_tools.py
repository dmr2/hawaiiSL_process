from fixedwidth import FixedWidth
import pandas as pd
import numpy as np
import glob
import sys

# Convert U Hawaii hourly sea level data to daily maximum
# Write a file for each tide gauge with daily max tide values
META_CONFIG = {

    'number': {
        'required': True,
        'type': 'string',
        'start_pos': 1,
        'end_pos': 3,
        'alignment': 'right',
        'padding': ' '
    },

    'version': {
        'required': True,
        'type': 'string',
        'start_pos': 4,
        'end_pos': 5,
        'alignment': 'right',
        'padding': ' '
    },

    'name': {
        'required': True,
        'type': 'string',
        'start_pos': 6,
        'end_pos': 24,
        'alignment': 'right',
        'padding': ' '
    },
    'region': {
        'required': True,
        'type': 'string',
        'start_pos':25,
        'end_pos': 44,
        'alignment': 'right',
        'padding': ' '
    },
    'year': {
        'required': True,
        'type': 'string',
        'start_pos':45,
        'end_pos': 49,
        'alignment': 'right',
        'padding': ' '
    },
    'lat': {
        'required': True,
        'type': 'string',
        'start_pos':50,
        'end_pos': 56,
        'alignment': 'right',
        'padding': ' '
    },
    'lon': {
        'required': True,
        'type': 'string',
        'start_pos':57,
        'end_pos': 64,
        'alignment': 'right',
        'padding': ' '
    },
    'time': {
        'required': True,
        'type': 'string',
        'start_pos':65,
        'end_pos': 69,
        'alignment': 'right',
        'padding': ' '
    },
    'method': {
        'required': True,
        'type': 'string',
        'start_pos':70,
        'end_pos': 71,
        'alignment': 'right',
        'padding': ' '
    },
    'offset': {
        'required': True,
        'type': 'integer',
        'start_pos':72,
        'end_pos': 76,
        'alignment': 'right',
        'padding': ' '
    },
    'datum': {
        'required': True,
        'type': 'string',
        'start_pos':77,
        'end_pos': 78,
        'alignment': 'right',
        'padding': ' '
    },
}


TIDE_CONFIG = {
    'number': {
        'required': True,
        'type': 'string',
        'start_pos':1,
        'end_pos': 3,
        'alignment': 'right',
        'padding': ' '
    },
    'version': {
        'required': True,
        'type': 'string',
        'start_pos':4,
        'end_pos': 5,
        'alignment': 'right',
        'padding': ' '
    },
    'name': {
        'required': True,
        'type': 'string',
        'start_pos':6,
        'end_pos': 11,
        'alignment': 'right',
        'padding': ' '
    },
    'year': {
        'required': True,
        'type': 'string',
        'start_pos':12,
        'end_pos': 15,
        'alignment': 'right',
        'padding': ' '
    },
    'month': {
        'required': True,
        'type': 'string',
        'start_pos':16,
        'end_pos': 17,
        'alignment': 'right',
        'padding': ' '
    },
    'day': {
        'required': True,
        'type': 'string',
        'start_pos':18,
        'end_pos': 19,
        'alignment': 'right',
        'padding': ' '
    },
    'half': {
        'required': True,
        'type': 'string',
        'start_pos':20,
        'end_pos': 20,
        'alignment': 'right',
        'padding': ' '
    },
    '1': {
        'required': True,
        'type': 'string',
        'start_pos':21,
        'end_pos': 25,
        'alignment': 'right',
        'padding': ' '
    },
    '2': {
        'required': True,
        'type': 'string',
        'start_pos':26,
        'end_pos': 30,
        'alignment': 'right',
        'padding': ' '
    },
    '3': {
        'required': True,
        'type': 'string',
        'start_pos':31,
        'end_pos': 35,
        'alignment': 'right',
        'padding': ' '
    },
    '4': {
        'required': True,
        'type': 'string',
        'start_pos':36,
        'end_pos': 40,
        'alignment': 'right',
        'padding': ' '
    },
    '5': {
        'required': True,
        'type': 'string',
        'start_pos':41,
        'end_pos': 45,
        'alignment': 'right',
        'padding': ' '
    },
    '6': {
        'required': True,
        'type': 'string',
        'start_pos':46,
        'end_pos': 50,
        'alignment': 'right',
        'padding': ' '
    },
    '7': {
        'required': True,
        'type': 'string',
        'start_pos':51,
        'end_pos': 55,
        'alignment': 'right',
        'padding': ' '
    },
    '8': {
        'required': True,
        'type': 'string',
        'start_pos':56,
        'end_pos': 60,
        'alignment': 'right',
        'padding': ' '
    },
    '9': {
        'required': True,
        'type': 'string',
        'start_pos':61,
        'end_pos': 65,
        'alignment': 'right',
        'padding': ' '
    },
    '10': {
        'required': True,
        'type': 'string',
        'start_pos':66,
        'end_pos': 70,
        'alignment': 'right',
        'padding': ' '
    },
    '11': {
        'required': True,
        'type': 'string',
        'start_pos':71,
        'end_pos': 75,
        'alignment': 'right',
        'padding': ' '
    },
    '12': {
        'required': True,
        'type': 'string',
        'start_pos':76,
        'end_pos': 80,
        'alignment': 'right',
        'padding': ' '
    },
}


META_CONFIG_MON = {
    'number': {
        'required': True,
        'type': 'string',
        'start_pos': 1,
        'end_pos': 3,
        'alignment': 'right',
        'padding': ' '
    },
    'version': {
        'required': True,
        'type': 'string',
        'start_pos': 4,
        'end_pos': 5,
        'alignment': 'right',
        'padding': ' '
    },
    'name': {
        'required': True,
        'type': 'string',
        'start_pos': 6,
        'end_pos': 24,
        'alignment': 'right',
        'padding': ' '
    },
    'region': {
        'required': True,
        'type': 'string',
        'start_pos':25,
        'end_pos': 44,
        'alignment': 'right',
        'padding': ' '
    },
    'yr1': {
        'required': True,
        'type': 'string',
        'start_pos':45,
        'end_pos': 48,
        'alignment': 'right',
        'padding': ' '
    },
    'dash': {
        'required': True,
        'type': 'string',
        'start_pos':49,
        'end_pos': 49,
        'alignment': 'right',
        'padding': ' '
    },
    'yr2': {
        'required': True,
        'type': 'string',
        'start_pos':50,
        'end_pos': 54,
        'alignment': 'right',
        'padding': ' '
    },
    'lat': {
        'required': True,
        'type': 'string',
        'start_pos':55,
        'end_pos': 61,
        'alignment': 'right',
        'padding': ' '
    },
    'lon': {
        'required': True,
        'type': 'string',
        'start_pos':62,
        'end_pos': 69,
        'alignment': 'right',
        'padding': ' '
    },
    'method': {
        'required': True,
        'type': 'string',
        'start_pos':70,
        'end_pos': 71,
        'alignment': 'right',
        'padding': ' '
    },
    'offset': {
        'required': True,
        'type': 'string',
        'start_pos':72,
        'end_pos': 76,
        'alignment': 'right',
        'padding': ' '
    },
    'datum': {
        'required': True,
        'type': 'string',
        'start_pos':77,
        'end_pos': 78,
        'alignment': 'right',
        'padding': ' '
    },
}

def fmtll(latStr,lonStr):

    if len(latStr) < 6:
      diff = 6 - len(latStr)
      latStr = (diff*' ') + latStr
    if len(lonStr) < 7:
      diff = 7 - len(lonStr)
      lonStr = (diff*' ') + lonStr

    lat = int(latStr[0:2]) + int(latStr[2:4])/60. + int(latStr[4:5])/60.
    if latStr[-1] == "S":
      lat = -1*lat
    lon = int(lonStr[0:3]) + int(lonStr[3:5])/60. + int(lonStr[5:6])/60.
    if lonStr[-1] == "W":
      lon = -1*lon

    return lat,lon


def getList(path):

    fils = glob.glob(path)
    parts = [fil.strip('.dat').split('/')[-1] for fil in fils]
    gauge_list = set([fil[1:5] for fil in parts])


    return gauge_list


def getDailyMax(fil):

    # Get meta info for this station
    fw = FixedWidth(META_CONFIG)
 
    # Get number of observations
    nday = (sum(1 for line in open(fil,'rb')) - 1)/2

    # read in observations
    f = open(fil, 'rb')
    header = f.readline()
    meta = fw._string_to_dict(header)

    fw = FixedWidth(TIDE_CONFIG)

    cols = ['Gauge','Name','Lat','Lon','Method','Datum','Offset','Year','Month','Day','Max_Tide']
    dfOut = pd.DataFrame(columns=cols)

    charOut = np.empty((nday,len(cols)),dtype=object)

    lat,lon = fmtll(meta['lat'],meta['lon'])

    date_last = -9999
    nobs_last = -9999
    i = 0
    for line in f:
        parts = fw._string_to_dict(line)
        lvls = [int(parts[str(ii)]) for ii in range(1, 13)]

        if meta['datum'] == 'X': 
          lvls = [9999 for jj in lvls] # these data are not referenced to a datum

        date = parts['year']+parts['month']+parts['day']
        if date == date_last:
          this_max = np.max(lvls)
          if this_max == 9999:
            this_max = np.nan
    
          if (nobs_last + sum([lvls[ii]!=9999 for ii in range(len(lvls))])) < 12:
            dayMax = -999
          else:
            dayMax = np.max([this_max,max_last])
            if np.isnan(dayMax): dayMax = -999 

          charOut[i,:] = [meta['number']+meta['version'],meta['name'],"{0:.2f}".format(lat),"{0:.2f}".format(lon),meta['method'], \
                          meta['datum'], meta['offset'],parts['year'],parts['month'],parts['day'],str(dayMax)]

          i+=1
        else:
          nobs_last = sum([lvls[ii]!=9999 for ii in range(len(lvls))])
          max_last = np.max(lvls)
          if max_last == 9999:
            max_last = np.nan
          date_last = date
    
    #return dfOut,int(str(date)[0:4]),meta
    return charOut,int(str(date)[0:4]),meta


def recordQA(arr,y1,y2,threshold):

     # Determine if this gauge meets the criteria
     cnt = 0
     for row in arr:
       if (float(row[7]) >= y1 and float(row[7]) <= y2):
         if int(row[10]) != -999:
           cnt += 1
     frac = cnt/((y2-y1+1)*365.25)
     if frac >= threshold:
       check = True
     else:
       check = False
        
     return check, frac

def recordQAmon(arr,y1,y2,threshold):

     # Determine if this gauge meets the criteria
     cnt = 0
     first_yr = int(row[4])
     for row in arr:
       if (int(row[4]) >= y1 and int(row[4]) <= y2):
         if int(row[6]) != -999:
           cnt += 1
     frac = cnt/float((y2-y1+1)*12)
     if frac >= threshold and first_yr >= y1:
       check = True
     else:
       check = False
        
     return check, frac

def getMonMean(fil):

     print "Opening file: %s" %fil
     fw = FixedWidth(META_CONFIG_MON)
 
     # determine how many years we will read
     f = open(fil, 'rb')
     header = f.readline()
     all_years = [int(line[0:12].strip()) for line in f]

     # read in observations
     f = open(fil, 'rb')
     header = f.readline()
     meta = fw._string_to_dict(header)

     nlin = (max(all_years) - min(all_years) + 1)*12
     charOut = np.empty((nlin,7),dtype=object)

     lat,lon = fmtll(meta['lat'],meta['lon'])

     i = 0
     nmiss = 0
     _sum = 0.
     this_mon = 1
     cnt = 0
     for ii,line in enumerate(f):

         line = line.split()
         mon = int(line[1])

         if mon == this_mon:
            year = line[0]
            if line[3] == '9999' or meta['datum'] == 'X':
              nmiss += 1
            else:
              _sum = _sum + float(line[3])
              cnt += 1
         else:

            # The monthly values are calculated from the daily data with a
            # simple average of all the daily values in a month. If seven or
            # fewer values are missing, the monthly value is calculated.  
            if (nmiss <= 7): 
               avg = _sum / float(cnt)
            else:
               avg = -999
            charOut[i,:] = [meta['number']+meta['version'],meta['name'],"{0:.2f}".format(lat),"{0:.2f}".format(lon), \
                            year,str(this_mon).zfill(2),str(int(avg))]
            nmiss = 0
            _sum = 0.
            cnt = 0
            this_mon = mon
            i += 1

     if (nmiss <= 7): 
        avg = _sum / float(cnt)
     else:
        avg = -999
     charOut[i,:] = [meta['number']+meta['version'],meta['name'],"{0:.2f}".format(lat),"{0:.2f}".format(lon), \
                     year,str(this_mon).zfill(2),str(int(avg))]

     return charOut,meta

def getMaxRecord(arr,search_length,threshold):

      check = False
      year_list = list(arr[:,4])
      yr1_rec = int(min(year_list))
      yr2_rec = int(max(year_list))
      frac = -999 
      y1 = yr1_rec
      y2 = yr2_rec
      record_length = yr2_rec - yr1_rec + 1

      if record_length >= search_length:
        
        # get list of start and end years to check
        period_list = [[i,i+(search_length-1)] for i in range(yr1_rec,yr2_rec) if i+(search_length-1) <= yr2_rec]

        yr1 = 9999
        yr2 = -9999
        frac_max = 0.

        # search these periods
        for pair in period_list:
          indx_start = year_list.index(str(pair[0]))
          indx_end = year_list.index(str(pair[1])) + 12

          # Number of missing observations
          num_missing = sum(arr[indx_start:indx_end,6] == '-999')
      
          frac = 1 - num_missing/float(indx_end-indx_start+1)
          
          frac_max = max(frac_max, frac)
          if frac_max == frac:
            yr1 = pair[0]
            yr2 = pair[1]

        if frac_max > threshold:
           check = True
        else:
           check = False

      return (check, frac_max, yr1, yr2)

def getMaxRecordDaily(arr,search_length,threshold):

      check = False
      year_list = list(arr[:,7])
      yr1_rec = int(min(year_list))
      yr2_rec = int(max(year_list))
      frac = -999 
      y1 = yr1_rec
      y2 = yr2_rec
      record_length = yr2_rec - yr1_rec + 1

      if record_length >= search_length:
        
        # get list of start and end years to check
        period_list = [[i,i+(search_length-1)] for i in range(yr1_rec,yr2_rec) if i+(search_length-1) <= yr2_rec]

        yr1 = 9999
        yr2 = -9999
        frac_max = 0.

        # search these periods
        for pair in period_list:

          #print "Checking period %s -- %s ..." %(str(pair[0]),str(pair[1]))

          indx_start = year_list.index(str(pair[0]))
          indx_end = year_list.index(str(pair[1])) + 12

          # Number of missing observations
          num_missing = sum(arr[indx_start:indx_end,10] == '-999')
      
          frac = 1 - num_missing/float(indx_end-indx_start+1)
          
          frac_max = max(frac_max, frac)
          if frac_max == frac:
            yr1 = pair[0]
            yr2 = pair[1]

        if frac_max > threshold:
           check = True
        else:
           check = False

      return (check, frac_max, yr1, yr2)
