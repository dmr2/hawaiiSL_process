c..  rqdsday.f      
c..  read in 'Archive" Format  daily sea level data create 
c..  two column format output  time(year)  and height(in millimeter).  
c..  input (infile) : put in input file name             (e.g. d001a.dat) 
c..  output(outfile): internally created from input file (e.g. d001a.out)
c..  execute as e.g. " rqdsday.x d001a.dat "  
c..
      character*50 infile,outfile,name
      character*5  fname
      real*8       t
      integer m, d
      dimension    idata(12)

C*** if command line input is not allowed change replace by next 2 statements
c      write(6,*) ' put the input file name e.g. d001a.dat '
c      read(5,'(a50)') infile

      iarg=1
      call getarg(iarg, infile)

c.. opening input file 
      open(unit=15,file=infile)

      read(15,'(a50)') name
 7100 format(a50)
      read(infile, '(a5)') fname
      write(6,' ( a50) ') name
      write(outfile,8000) fname
 8000 format(a5,'.out')
      open(unit=30, file=outfile)
      read(15,7000) jyear     
      write(6,*) 'starting year = ', jyear
      alim=365. 
      if (jyear .eq. 1900) then
         alim=365. 
      else if (mod(jyear,4).eq.0) then
         alim=366.
      end if
      back space 15
c.. start reading in daily data one record at a time

      jday = 1
 0001 read(15,7000,end=9000) iyear,jl, idata 
 7000 format(10x,i4,1x,i3,2x,12i5)
      if ( iyear .eq. jyear ) then
         jh=jl+11
         if(jh.gt.365) then
            jh=nint(alim)
         end if
         do 10 j=jl,jh
c            t=dble(iyear) + dble(j-0.5)/alim
            call doy2greg(jday, iyear, m, d)
            write(30, *) iyear, m, d, idata(j-jl+1)
            jday = jday + 1
 0010    continue
      else 
         jday = 1
         jyear = iyear
         alim=365.
         if (jyear .eq. 1900) then
            alim=365.
         else if (mod(jyear,4) .eq. 0) then
            alim=366.
         end if 
         back space 15
      end if
      go to 1
 9000 stop
      end
