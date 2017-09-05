#!/bin/sh

export DATAPATH
DATAPATH=/ucn/orithyia_data/wschreyer/MCNP/MCNP_DATA

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > ucn_$PBS_ARRAYID.mcnp
/ucn/orithyia_data/wschreyer/MCNP/MCNP_CODE/bin/mcnp6 inp=ucn_$PBS_ARRAYID.mcnp outp=out$PBS_ARRAYID runtpe=/ucnscr/run$PBS_ARRAYID mctal=tal$PBS_ARRAYID
rm ucn_$PBS_ARRAYID.mcnp
rm /ucnscr/run$PBS_ARRAYID

