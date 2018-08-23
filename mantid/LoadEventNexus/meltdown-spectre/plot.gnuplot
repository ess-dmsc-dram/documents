set term pdf size 8,6
set term png enh size 2400,1800
set outp "meltdown-spectre.png"

set yla "events/s"
set xla "MPI ranks"
set xra [0.5:12.5]
set yra [0:]
set xtics 1,1
set key t l

# for i in $(seq 1 12); do echo -n "$i "; cat before-ranks-"$i"-uncompressed | statistics.py -c 4 -u; done > before-uncompressed
# for i in $(seq 1 12); do echo -n "$i "; cat after-ranks-"$i"-uncompressed | statistics.py -c 4 -u; done > after-uncompressed
# for i in $(seq 1 12); do echo -n "$i "; cat before-ranks-"$i"-compressed | statistics.py -c 4 -u; done > before-compressed
# before is 4.4.0-83-generic
events=22065736
set title "DMSC workstation, 12 cores / 24 threads, SSD, 220 M events"
p \
  "before-uncompressed" u 1:(10*events/$2):(10*events*$4/$2/$2)  w yerrorb  ti "before" , \
  "after-uncompressed" u 1:(10*events/$2):(10*events*$4/$2/$2)  w yerrorb  ti "after" , \
  "before-compressed" u 1:(10*events/$2):(10*events*$4/$2/$2)  w yerrorb  ti "before, compressed file" 
#p \
#  "before-uncompressed" u 1:2:4  w yerrorb ls 100
