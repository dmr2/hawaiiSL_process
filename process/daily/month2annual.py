import sys
import glob
from import_tools import *

# Convert U Hawaii monthly means to annual values

# Write a file for each tide gauge with annual means

# The annual mean values are calculated from the monthly data
# with a simple average of all the monthly values in a year.
# If two or few monthly values are missing, the annual average 
# is calculated.


root = '/Users/dmr/hawaiiSL'

basin_list = ['atlantic','indian','pacific']

allsite_fil = 'uhawaii_sites_dmr.dat'

f = open(allsite_fil, 'rb')
lines=f.readlines()
master_list=[]
for x in lines:
    master_list.append(x.split(' ')[1].strip(';'))
f.close()

for basin in basin_list:

  # List of tide gauges for this basin
  fils = glob.glob(root+'/monthly/'+basin+'/monthly_sl_'+basin+'_*.tsv')
  parts = [fil.strip('.tsv').split('/')[-1] for fil in fils]
  gauge_list = [fil.split('_')[3] for fil in parts]

  for i,gauge in enumerate(gauge_list):

    # list of yearly files for this gauge
    fil = glob.glob(root+'/monthly/'+basin+'/monthly_sl_'+basin+'_'+gauge+'_*.tsv')[0]

    f = open(fil, 'rb')
    header = f.readline()

    years = []
    heights = []

    i = 0
    nmiss = 0
    _sum = 0.
    cnt = 0
    for ii,line in enumerate(f):

        line = line.strip('\n')
        line = line.split('\t')
        yr = int(line[4])


        if line[6] == '-999':
          nmiss += 1
        else:
          _sum = _sum + float(line[6])
          cnt += 1

        nobs = cnt + nmiss
        if nobs == 12:
          if (nmiss <= 3): 
             avg = _sum / float(cnt)
          else:
           avg = -99999

          years.append(yr)
          heights.append(avg)

          nmiss = 0
          _sum = 0.
          cnt = 0
     
    # Only write if this site is in the master list...

    if gauge.upper() in master_list:
      gauge_out = str(gauge)[0:3]+"00000" 
      outf =  open('rlr_annual/'+gauge_out+'.rlrdata', 'wb')
      for i,iyr in enumerate(years):
        outf.write('%4i;%6i;%1s;%3s\n' %(int(years[i]),heights[i],"N","000"))

#monthly/atlantic/monthly_sl_atlantic_722a_2011-2013.tsv
#
#Gauge   Name    Lat     Lon     Year    Month   Height
#722A    Tristan da Cunha        -37.05  -12.30  2011    01      -999
#722A    Tristan da Cunha        -37.05  -12.30  2011    02      2236
#722A    Tristan da Cunha        -37.05  -12.30  2011    03      -999
#722A    Tristan da Cunha        -37.05  -12.30  2011    04      -999


#1695.rlrdata
# 1986;  7019;N;000
# 1987;-99999;N;000
# 1988;  7036;N;000
# 1989;  6989;N;000


#'%4n;%6n;%1c;%1n%1n%1n'





