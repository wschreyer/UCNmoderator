#!/bin/sh

#SBATCH --time=2
#SBATCH --mem=500M

MCNP_PATH=/home/wschreye/MCNP
TMP=/home/wschreye/scratch

rm slurm-*
$MCNP_PATH/MCNP_CODE/bin/merge_mctal $TMP/tal*
$MCNP_PATH/MCNP_CODE/bin/merge_mesh_tal_one -i $TMP/meshtal*
mv $TMP/out1 out1
python writeREADME.py > README.md
rm $TMP/out* $TMP/tal* $TMP/meshtal*
#param=$(grep '^Cylindrical D2O' README.md | cut -d ' ' -f 14)
#git add MCTALMRG MESHTALMRG README.md out1 ucn.inp ucn.mcnp
#git commit -m "Changed target offset to ${param}cm"
