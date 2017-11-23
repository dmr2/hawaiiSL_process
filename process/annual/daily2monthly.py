#!/usr/bin/python

import sys
import glob
from import_tools import *

# Convert U Hawaii daily sea-level data to monthly means

# Write a file for each tide gauge with month means

# The monthly values are calculated from the daily data with a
# simple average of all the daily values in a month. If seven or
# fewer values are missing, the monthly value is calculated.  


root = '/Users/dmr/hawaiiSL'
threshold = .85 # fraction of data needed

basin_list = ['atlantic','indian','pacific']

for basin in basin_list:

  # Store meta data for each site
  cols = ['Gauge','Short_Name','Lat','Lon','Long_Name','Region','Record_Start', \
          'Record_End','N_Obs','QA_YR1','QA_YR2','QA_Yrs','QA_frac','QA_Pass']

  metaAll = pd.DataFrame(columns=cols)

  # List of tide gauges for this basin
  gauge_list = getList(root+'/'+basin+'/daily/formatted/*.out')

  for i,gauge in enumerate(gauge_list):

    # list of yearly files for this gauge
    gauge_fils = glob.glob(root+'/'+basin+'/daily/formatted/*'+gauge+'*.out')
    #gauge_fils = glob.glob(root+'/'+basin+'/daily/formatted/*217*.out')

    for j,fil in enumerate(gauge_fils):

      arr, meta  = getMonMean(fil)

      # Concatenate observations

      # initialize
      if j == 0:
        arrAll = arr
      else:
        # Do we need to fill in missing values?
        last_arr_last = arrAll[:,4][-1]
        this_arr_first = arr[:,4][0]

        diff = int(this_arr_first) - int(last_arr_last) - 1
        if diff > 0:
          filler = np.empty((diff*12,7),dtype=object)
          fill_years = range(int(last_arr_last) + 1, int(this_arr_first))
         
          ii=0
          for fillyr in fill_years:
             for mon in range(1,12+1):
                 filler[ii,0:4] = arr[1,0:4]
                 filler[ii,4] = str(fillyr)
                 filler[ii,5] = str(mon).zfill(2)
                 filler[ii,6] = '-999'
                 ii += 1
          arrAll = np.concatenate((arrAll, filler), axis=0)
          arrAll = np.concatenate((arrAll, arr), axis=0)
        elif diff < 0:
          # There may be duplicate/overlapping years
         
          # Find the overlapping years and remove them
          years = set(arrAll[:,4]).intersection(arr[:,4])
          indx = np.in1d(arr[:,4],list(years),invert=True)

          if arr[indx,:].size != 0:
            arrAll = np.concatenate((arrAll, np.squeeze(arr[indx,:])), axis=0)
        else:
          arrAll = np.concatenate((arrAll, arr), axis=0)

    nobs = sum(arrAll[:,6]!=-999)
    lat,lon = fmtll(meta['lat'],meta['lon'])

    # determine longest observation period that meets criteria
    yr1 = int(min(arrAll[:,4]))
    yr2 = int(max(arrAll[:,4]))

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
        num_missing = sum(arrAll[:,6] == '-999')
        frac = 1 - num_missing/float(record_length*12)
        if frac >= threshold:
          check = True
          y1_recmax = yr1
          y2_recmax = yr2
        else: 
        # Search for longest period that meets threshold
          for jj in range(record_length,1,-1):
           if check == False:
             check,frac,y1_recmax,y2_recmax = getMaxRecord(arrAll,jj,threshold)

    if (y2_recmax-y1_recmax+1) < 30: 
      check = False
      frac = -999

    metaAll.loc[i] = pd.Series({'Gauge':meta['number']+meta['version'],'Short_Name':meta['name'][0:4],'Lat':"{0:.2f}".format(lat),
                                'Lon':"{0:.2f}".format(lon),'Long_Name':meta['name'],'Region':meta['region'],'Record_Start':yr1,
                                'Record_End':yr2,'N_Obs':nobs,'QA_YR1':y1_recmax,'QA_YR2':y2_recmax,'QA_Yrs':(y2_recmax-y1_recmax+1),
                                'QA_frac':"{0:.2f}".format(frac),'QA_Pass':check})

    outFil = './monthly/'+basin+'/monthly_sl_'+basin+'_'+meta['number']+meta['version'].lower()+'_'+str(yr1)+'-'+str(yr2)+'.tsv'
    print "Writing: %s" %outFil
    cols = 'Gauge\tName\tLat\tLon\tYear\tMonth\tHeight'

    with open(outFil,'wb') as f:
      np.savetxt(f,arrAll,delimiter='\t',header=cols,fmt='%s',comments='')
    #dfAll.to_csv(outFil,index=False,sep='\t')
 
  outFil = './monthly/'+basin+'/mon_meta.tsv'
  print "Writing: %s" %outFil
  metaAll.to_csv(outFil,index=False,sep='\t')
