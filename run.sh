#!/bin/sh

export DATAPATH
DATAPATH=/ucn/orithyia_data/wschreyer/MCNP/MCNP_DATA

sed -e "s/MYSEED/`date +%N | tail -c 6`/g" ucn.mcnp > ucn_$PBS_ARRAYID.mcnp
/ucn/orithyia_data/wschreyer/MCNP/MCNP_CODE/bin/mcnp6 inp=ucn_$PBS_ARRAYID.mcnp outp=out$PBS_ARRAYID runtpe=/ucnscr/run$PBS_ARRAYID mctal=tal$PBS_ARRAYID
rm ucn_$PBS_ARRAYID.mcnp
rm /ucnscr/run$PBS_ARRAYID


export FLUPRO=/home/wschreyer/fluka2011.2c-6

sed -e "s/MYSEED/`date +%N | tail -c 6`./g" ucn.inp > ucn_$PBS_ARRAYID.inp
$FLUPRO/flutil/rfluka -N0 -M1 -e clusterfluka ucn_$PBS_ARRAYID
rm ucn_$PBS_ARRAYID.inp

