# hawaiiSL_process: UHawaii Sea Level Center sea level processing code for Rasmussen et al. (submitted)

README file last updated by DJ Rasmussen, dmr2-at-princeton-dot-edu, Wed Nov 22 17:51:19 MST 2017

## Citation

This code is intended to accompany the results of:

D.J. Rasmussen, K. Bittermann, M.K. Buchanan, S. Kulp, B.H. Strauss, R.E. Kopp and M. Oppenheimer:
Coastal flood implications of 1.5 °C, 2.0 °C, and 2.5 °C temperature stabilization 
targets in the 21st and 22nd century. ArXiv e-prints. eprint: 1710.08297.


Before running scripts, the QC'd hourly SL data must be obtained from:
<ftp://ftp.soest.hawaii.edu/uhslc/rqds/global.zip> (~600 MB; Last updated: 11/13/17, 4:57:00 AM)

### data
* **unzip.py** Unzip hourly U Hawaii SL Center data
* **global.tgz** Daily maximum SL data (i.e., output from **hourly2dailyMax.py**)

### process
* **hourly2dailyMax.py** Convert hourly U Hawaii SL data to daily maximums

----

    Copyright (C) 2017 by D.J. Rasmussen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
