#!/bin/sh

export FLUPRO=/home/wschreyer/fluka2011.2c-6
cd /home/wschreyer/scratch/flukasims
$FLUPRO/flutil/rfluka -N0 -M1 -e clusterfluka fluka_RUN
rm fluka_RUN.inp
rm job_RUN.sh

