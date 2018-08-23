set term pdf enh size 7,4
#set term png enh size 1200,900
set outp "LoadEventNexus.pdf"

set yla "events/s"
set xla "MPI ranks"
set xra [0.5:12.5]
set yra [0:]
set xtics 1,1
set key t l

events=22065736


set title "Dual Socket Haswell (Intel Xeon E5-2620 v3 @ 2.40GHz), 12 cores / 24 threads, SSD, 22 M events"
p \
  "PG3_4871-1x-uncompressed" u ($0+1):(events/$5) w p ti "MPI loader" ls 210, \
  "PG3_4871-1x"              u ($0+1):(events/$5) w p ti "MPI loader, compressed file" ls 100, \
  events/1.52 ti "threaded Mantid loader" ls 210, \
  events/4.36 ti "threaded Mantid loader, compressed file" ls 100

set title "Dual Socket Haswell (Intel Xeon E5-2620 v3 @ 2.40GHz), 12 cores / 24 threads, SSD, 220 M events"
p \
  "PG3_4871-10x-uncompressed" u ($0+1):(10*events/$5) w p ti "MPI loader" ls 210, \
  "PG3_4871-10x"              u ($0+1):(10*events/$5) w p ti "MPI loader, compressed file" ls 100, \
  10*events/6.94 ti "threaded Mantid loader" ls 210, \
  10*events/24.19 ti "threaded Mantid loader, compressed file" ls 100

set title "Dual Socket Haswell (Intel Xeon E5-2620 v3 @ 2.40GHz), 12 cores / 24 threads, SSD, 2200 M events"
p \
  "PG3_4871-100x-uncompressed" u ($0+1):(100*events/$5) w p ti "MPI loader" ls 210, \
  "PG3_4871-100x"              u ($0+1):(100*events/$5) w p ti "MPI loader, compressed file" ls 100, \
  100*events/55.66 ti "threaded Mantid loader" ls 210, \
  100*events/201.58 ti "threaded Mantid loader, compressed file" ls 100

#events=220657360
#
#set title "DMSC workstation, 12 cores / 24 threads, SSD"
#p \
#  "preliminary-results" u 1:(events/$4) w p ti "MPI loader" ls 210, \
#  "preliminary-results" u 1:(events/$5) w p ti "MPI loader, compressed file" ls 100, \
#  events/5.1 ti "threaded Mantid loader" ls 210, \
#  events/20.5 ti "threaded Mantid loader, compressed file" ls 100

#set title "DMSC workstation, 12 cores / 24 threads, cached file"
#p \
#  "preliminary-results" u 1:(events/$2) w p ti "MPI loader" ls 101, \
#  "preliminary-results" u 1:(events/$3) w p ti "MPI loader, compressed file" ls 201, \
#  events/3.3 ti "current threaded Mantid loader" ls 110, \
#  events/17.5 ti "current threaded Mantid loader, compressed file" ls 210
