import sys
import glob
import os
from import_tools import *

# Convert U Hawaii monthly means to annual values

# Write a file for each tide gauge with annual means

# The annual mean values are calculated from the monthly data
# with a simple average of all the monthly values in a year.
# If two or few monthly values are missing, the annual average 
# is calculated.


root = '/Users/dmr/HawaiiSL 2017/data/global'

basin_list = ['atlantic','indian','pacific']

for basin in basin_list:

  if not os.path.exists(root+'/'+basin+'/annual/'):
    os.makedirs(root+'/'+basin+'/annual/')
  # List of tide gauges for this basin
  fils = glob.glob(root+'/'+basin+'/monthly/monthly_sl_'+basin+'_*.tsv')
  parts = [fil.strip('.tsv').split('/')[-1] for fil in fils]
  gauge_list = [fil.split('_')[3] for fil in parts]

  for i,gauge in enumerate(gauge_list):

    # list of yearly files for this gauge
    fil = glob.glob(root+'/'+basin+'/monthly/monthly_sl_'+basin+'_'+gauge+'_*.tsv')[0]

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
     
    # Write out file
    outf =  open(root+'/'+basin+'/annual/annual_sl_'+basin+'_'+gauge+'_'+str(min(years))+'-'+str(max(years))+'.tsv', 'wb')
    for i,iyr in enumerate(years):
      outf.write('%4i;%6i;%1s;%3s\n' %(int(years[i]),heights[i],"N","000"))

