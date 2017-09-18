#!/bin/sh

#$ -l short=TRUE

MCNP_PATH=/nfs/mds/tmp/no72lum/MCNP

rm run.sh.*
rm prerun.sh.*
$MCNP_PATH/MCNP_CODE/bin/merge_mctal tal*
$MCNP_PATH/MCNP_CODE/bin/merge_mesh_tal_one -i meshtal*
python writeREADME.py > README.md
rm out{2..250}
rm tal*
rm meshtal*
param=$(echo "`grep '^D2O:' README.md | cut -d ' ' -f 2` - `grep '^LD2:' README.md | cut -d ' ' -f 2` - 9" | bc)
git add MCTALMRG MESHTALMRG README.md out1 ucn.inp ucn.mcnp
git commit -m "Changed top thickness of D2O to ${param}cm"
