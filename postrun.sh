#!/bin/sh

#SBATCH --time=5
#SBATCH --mem=2000M
#SBATCH --cpus-per-task=8

MCNP_PATH=/home/wschreye/MCNP
TMP=/home/wschreye/scratch

python mergeTallies.py $TMP/*.root

#$MCNP_PATH/MCNP_CODE/bin/merge_mctal $TMP/tal*
#merge_meshtal $TMP/meshtal*
python writeREADME.py > README.md
./plot.sh
rm slurm-*
#rm $TMP/out* $TMP/tal* $TMP/meshtal*
param=$(grep M43 out1 | tr -s ' ' | cut -d ' ' -f 6)
git add README.md out1 ucn.inp ucn.mcnp tallies.root
git commit -m "Added ${param}% ortho-H2 contamination to ortho-D2"
