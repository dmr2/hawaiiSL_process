#!/bin/bash

# Converts daily, row-based, U Hawaii SL files to daily, column-based files

root="/Users/dmr/HawaiiSL 2017/data/global"


for basin in atlantic pacific indian
do

cd "$root/$basin/daily/"
FILES=*.dat

mkdir row2col

for f in $FILES
do

  /Users/dmr/HawaiiSL\ 2017/process/daily/rqdsday.exe $f

# insert meta data in first row of file
  fbname=$(basename "$f" .dat)

  head -n 1 $f | cat - ${fbname}.out > temp && mv temp row2col/${fbname}.out
  rm ${fbname}.out

done
done
