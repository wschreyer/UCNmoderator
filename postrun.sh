#!/bin/sh

rm run.sh.*
rm prerun.sh.*
/ucn/orithyia_data/wschreyer/MCNP/MCNP_CODE/bin/merge_mctal tal*
/ucn/orithyia_data/wschreyer/MCNP/MCNP_CODE/bin/merge_mesh_tal_one -i meshtal*
python writeREADME.py > README.md
rm out{2..100}
rm tal*
rm meshtal*
param=$(grep 'Lead - D2O' README.md | cut -d ' ' -f 4)
git add MCTALMRG MESHTALMRG README.md out1 ucn.inp ucn.mcnp
git commit -m "Changed thickness of lead shield to ${param}cm"
