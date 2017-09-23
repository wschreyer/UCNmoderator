#!/bin/sh

#SBATCH --time=1
#SBATCH --mem=500M

MCNP_PATH=/home/wschreye/MCNP

rm slurm-*
$MCNP_PATH/MCNP_CODE/bin/merge_mctal tal*
$MCNP_PATH/MCNP_CODE/bin/merge_mesh_tal_one -i meshtal*
python writeREADME.py > README.md
rm out{2..500}
rm tal*
rm meshtal*
param=$(echo "`grep '^He-II:' README.md | cut -d ' ' -f 3` - 1.3" | bc)
git add MCTALMRG MESHTALMRG README.md out1 ucn.inp ucn.mcnp
git commit -m "Changed radius of He-II to ${param}cm"
