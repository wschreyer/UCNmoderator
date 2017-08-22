#!/bin/sh

export FLUPRO=/home/wschreyer/fluka2011.2c-6

sed -e "s/MYSEED/`date +%N | tail -c 6`./g" ucn.inp > ucn_$PBS_ARRAYID.inp
$FLUPRO/flutil/rfluka -N0 -M1 -e clusterfluka ucn_$PBS_ARRAYID
rm ucn_$PBS_ARRAYID.inp

