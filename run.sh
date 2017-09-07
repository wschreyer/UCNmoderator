#!/bin/sh

echo "Running on $PBS_O_HOST"
if [ $PBS_O_HOST = 'angerona.triumf.ca' ]
then
  MCNP_PATH=/ucndata/MCNP
else
  MCNP_PATH=/ucn/orithyia_data/wschreyer/MCNP
fi
export DATAPATH=$MCNP_PATH/MCNP_DATA

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > ucn_$PBS_ARRAYID.mcnp
$MCNP_PATH/MCNP_CODE/bin/mcnp6 inp=ucn_$PBS_ARRAYID.mcnp outp=out$PBS_ARRAYID runtpe=/ucnscr/run$PBS_ARRAYID mctal=tal$PBS_ARRAYID
rm ucn_$PBS_ARRAYID.mcnp
rm /ucnscr/run$PBS_ARRAYID

