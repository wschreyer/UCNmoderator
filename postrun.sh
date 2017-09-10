#!/bin/sh

rm run.sh.*
rm prerun.sh.*
/ucn/orithyia_data/wschreyer/MCNP/MCNP_CODE/bin/merge_mctal tal*
/ucn/orithyia_data/wschreyer/MCNP/MCNP_CODE/bin/merge_mesh_tal_one -i meshtal*
python writeREADME.py > README.md
rm out{2..100}
rm tal*
rm meshtal*

