#!/bin/sh

#SBATCH --time=5
#SBATCH --mem=2000M
#SBATCH --cpus-per-task=8

MCNP_PATH=/home/wschreye/MCNP
TMP=/home/wschreye/scratch

python mergeTallies.py $TMP/*.root
python writeREADME.py > README.md
./plot.sh
rm slurm-*
param=$(grep 'LD2 - HE-II:' README.md | cut -d ' ' -f 8)
git add README.md out1 ucn.inp ucn.mcnp tallies.root
git commit -m "Changed LD2 vacuum distance to ${param}cm"
