#!/bin/sh

#SBATCH --time=5
#SBATCH --mem=500M

MCNP_PATH=/home/wschreye/MCNP
export PATH=$MCNP_PATH/MCNP_CODE/bin/:$PATH
TMP=/home/wschreye/scratch

$MCNP_PATH/MCNP_CODE/bin/merge_mctal $TMP/tal*
merge_meshtal $TMP/meshtal*
mv $TMP/out1 out1
python writeREADME.py > README.md
rm slurm-*
rm $TMP/out* $TMP/tal* $TMP/meshtal*
#param=$(grep 'He-II - heat exchanger:' README.md | cut -d ' ' -f 5)
#git add MCTALMRG MESHTALMRG README.md out1 ucn.inp ucn.mcnp
#git commit -m "Changed heat exchanger distance to ${param}cm"
