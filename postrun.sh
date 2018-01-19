#!/bin/sh

#SBATCH --time=5
#SBATCH --mem=2000M
#SBATCH --cpus-per-task=8

MCNP_PATH=/home/wschreye/MCNP
TMP=/home/wschreye/scratch
module load root
module load python27-scipy-stack

python mergeTallies.py $TMP/*.root

python writeREADME.py > README.md
./plot.sh
rm slurm-*
param=$(echo "`grep '^D2O:' README.md | cut -d ' ' -f 3` - `grep '^LD2:' README.md | cut -d ' ' -f 3` - 0.5" | bc)
git add README.md out1 ucn.inp ucn.mcnp tallies.root
git commit -m "Changed radial thickness of D2O to ${param}cm"
