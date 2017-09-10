#!/bin/sh

echo "Running on `hostname`"
if [ `hostname` = 'angerona.triumf.ca' ] || [ `hostname` = 'lumi.triumf.ca' ] || [ `hostname` = 'skadi.triumf.ca' ]
then
  MCNP_PATH=/ucn/angerona_data/wschreyer/MCNP
else
  MCNP_PATH=/ucn/orithyia_data/wschreyer/MCNP
fi
export DATAPATH=$MCNP_PATH/MCNP_DATA

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > ucn_$PBS_ARRAYID.mcnp
rm -f out$PBS_ARRAYID /ucnscr/run$PBS_ARRAYID tal$PBS_ARRAYID meshtal$PBS_ARRAYID /ucnscr/mdata$PBS_ARRAYID
$MCNP_PATH/MCNP_CODE/bin/mcnp6 inp=ucn_$PBS_ARRAYID.mcnp outp=out$PBS_ARRAYID runtpe=/ucnscr/run$PBS_ARRAYID mctal=tal$PBS_ARRAYID meshtal=meshtal$PBS_ARRAYID mdata=/ucnscr/mdata$PBS_ARRAYID
rm ucn_$PBS_ARRAYID.mcnp
rm /ucnscr/run$PBS_ARRAYID
rm /ucnscr/mdata$PBS_ARRAYID
