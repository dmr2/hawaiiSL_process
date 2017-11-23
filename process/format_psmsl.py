import csv

psmslID = []
lat = []
lon = []
name = []
cID = []
sID = []



f = open('PSMSL_sites.dat','rb')

for line in f:
 if line[0:4].strip() == 'ID':
   continue
 elif line.strip() == '':
   continue
 else:
 
   try:
    cID1 =  int(line[32:36].strip())
   except:
    pass
   if line[0:5].strip() != '':

     psmslID.append(line[0:5].strip()) # ID
     sID.append(line[5:9].strip()) # SC
     name.append(line[9:51].strip()) # Station Name
     #print line[9:51].strip(),line[0:5].strip(),line[5:9].strip()

     lat1 =  float(line[51:61].strip())
     if line[61:62].strip() == 'S':
           lat1 *= -1

     lon1 = float(line[62:75].strip())
     if line[75:76].strip() == 'W':
           lon1 *= -1 

     lat.append(lat1)
     lon.append(lon1)
     cID.append(cID1)


flag = ['N']*len(cID)

outf =  open('psmsl_sites_dmr.dat', 'wb')
for i,site in enumerate(sID):
  outf.write('%5i;%11.6f;%12.6f; %-40s;%4i;%4i; %1s\n' % (int(psmslID[i]),lat[i],lon[i],name[i],int(cID[i]),int(sID[i]),flag[i]))

#with open('psmsl_sites_dmr.dat', 'wb') as outf:
#  writer = csv.writer(outf,delimiter = ';')
#  for i,site in enumerate(sID):
#
#    '%5n;%11.6f;%12.6f; %40c;%4n;%4n; %1c')
#    f.write('%-40s %6s %10s %2s\n' % (filename, type, size, modified))


#    writer.writerow([psmslID[i],lat[i],lon[i],name[i],cID[i],sID[i],"Y"])



