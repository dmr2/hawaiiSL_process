#!/usr/bin/python

import sys
import os
import glob
import calendar
from import_tools import *

# Convert U Hawaii hourly sea level data to daily maximum

# Write a file for each tide gauge with daily max tide values

root = '../data/global'
threshold = .8 # fraction of data needed for daily max

basin_list = ['pacific'] 
#basin_list = ['atlantic','indian','pacific']

for basin in basin_list:

  # Store meta data for each site
  cols = ['Gauge','Short_Name','Lat','Lon','Long_Name','Region','Record_Start', \
          'Record_End','N_Obs','QA_YR1','QA_YR2','QA_Yrs','QA_frac','QA_Pass']
  metaAll = pd.DataFrame(columns=cols)

  # List of tide gauges for this basin
  gauge_list = getList(root+'/'+basin+'/hourly/*.dat')

  for i,gauge in enumerate(gauge_list):

    # list of yearly files for this gauge
    gauge_fils = glob.glob(root+'/'+basin+'/hourly/*'+gauge+'*.dat')

    for j,fil in enumerate(sorted(gauge_fils)):
        print "Opening file: %s" %fil
        arr,year,meta = getDailyMax(fil)


        if j == 0:
          arrAll = arr
        else:
          # There may be gaps between files. We should fill in
          last_arr_last = arrAll[:,7][-1]
          this_arr_first = arr[:,7][0]

          diff = int(this_arr_first) - int(last_arr_last) - 1

          if diff > 0:
            fill_years = range(int(last_arr_last) + 1, int(this_arr_first))
            num_leap = sum([calendar.isleap(i) for i in fill_years])
            ndays = num_leap*366 + (len(fill_years) - num_leap)*365
            filler = np.empty((ndays,11),dtype=object)

            ii=0
            for fillyr in fill_years:
               for mon in range(1,12+1):
                 day_in_mon = calendar.monthrange(fillyr,mon)[1]
                 for day in range(1,day_in_mon+1):
                   filler[ii,0:7] = arr[1,0:7]
                   filler[ii,7] = str(fillyr)
                   filler[ii,8] = str(mon).zfill(2)
                   filler[ii,9] = str(day).zfill(2)
                   filler[ii,10] = '-999'
                   ii += 1
            arrAll = np.concatenate((arrAll, filler), axis=0)
            arrAll = np.concatenate((arrAll, arr), axis=0)
          elif diff < 0:
            # There may be duplicate/overlapping years

            # Find the overlapping years and remove them
            years = set(arrAll[:,7]).intersection(arr[:,7])
            indx = np.in1d(arr[:,7],list(years),invert=True)

            if arr[indx,:].size != 0:
              arrAll = np.concatenate((arrAll, np.squeeze(arr[indx,:])), axis=0)
          else:
            arrAll = np.concatenate((arrAll, arr), axis=0)

    nobs = sum(arrAll[:,10]!=-999)
    lat,lon = fmtll(meta['lat'],meta['lon'])

    # determine longest observation period that meets criteria
    yr1 = int(min(arrAll[:,7]))
    yr2 = int(max(arrAll[:,7]))

    record_length = (yr2-yr1+1)

    check = False
    if record_length < 30:
    # Fails if less than 30-years
      check = False
      frac = -999
      y1_recmax = yr1
      y2_recmax = yr2
    else:
      # First check the full record to see if it meets threshold
        num_missing = sum(arrAll[:,10] == '-999')
        frac = 1 - num_missing/float(len(arrAll[:,10]))
        if frac >= threshold:
          check = True
          y1_recmax = yr1
          y2_recmax = yr2
        else:
        # Search for longest period that meets threshold
          for jj in range(record_length,1,-1):
           if check == False:
             check,frac,y1_recmax,y2_recmax = getMaxRecordDaily(arrAll,jj,threshold)

    if (y2_recmax-y1_recmax+1) < 30:
      check = False
      frac = -999

    metaAll.loc[i] = pd.Series({'Gauge':meta['number']+meta['version'],'Short_Name':meta['name'][0:4],'Lat':"{0:.2f}".format(lat),
                                'Lon':"{0:.2f}".format(lon),'Long_Name':meta['name'],'Region':meta['region'],'Record_Start':yr1,
                                'Record_End':yr2,'N_Obs':nobs,'QA_YR1':y1_recmax,'QA_YR2':y2_recmax,'QA_Yrs':(y2_recmax-y1_recmax+1),
                                'QA_frac':"{0:.2f}".format(frac),'QA_Pass':check})
    
    outDir = root +'/'+basin+'/daily_max'
    if not os.path.exists(outDir):
      os.makedirs(outDir)

    outFil = outDir +'/dailymax_tide_'+basin+'_'+meta['number']+meta['version'].lower()+'_'+str(yr1)+'-'+str(yr2)+'.tsv'

    print "Writing: %s" %outFil
    cols = 'Gauge\tName\tLat\tLon\tMethod\tDatum\tOffset\tYear\tMonth\tDay\tMax_Tide'

    with open(outFil,'wb') as f:
      np.savetxt(f,arrAll,delimiter='\t',header=cols,fmt='%s',comments='')
    #dfAll.to_csv(outFil,index=False,sep='\t')
 
  outFil = outDir+'/'+basin+'_meta.tsv'

  print "Writing: %s" %outFil
  metaAll.to_csv(outFil,index=False,sep='\t')
