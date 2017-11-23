import glob
import zipfile
import os

root = "./"
basin_list = ['atlantic','pacific','indian']


for basin in basin_list:

  dir_name = root +"/"+ "global" +"/"+ basin +"/hourly"
  fils = glob.glob(dir_name + "/*")

  for fil in fils:
    zip = zipfile.ZipFile(fil)
    print "Extracting... %s", fil
    zip.extractall(dir_name)
    os.remove(fil)
