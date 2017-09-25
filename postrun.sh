#!/bin/sh

#SBATCH --time=2
#SBATCH --mem=500M

MCNP_PATH=/home/wschreye/MCNP

rm slurm-*
$MCNP_PATH/MCNP_CODE/bin/merge_mctal tal*
$MCNP_PATH/MCNP_CODE/bin/merge_mesh_tal_one -i meshtal*
python writeREADME.py > README.md
rm out{2..250}
rm tal*
rm meshtal*
param=$(grep 'LD2 - HE-II:' README.md | cut -d ' ' -f 4)
git add MCTALMRG MESHTALMRG README.md out1 ucn.inp ucn.mcnp
git commit -m "Changed thickness of LD2 to ${param}cm"
