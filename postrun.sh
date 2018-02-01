#!/bin/sh

#SBATCH --time=5
#SBATCH --mem=2000M
#SBATCH --cpus-per-task=8
#PBS -l walltime=00:05:00
#PBS -l nodes=1:ppn=8

MCNP_PATH=/home/wschreye/MCNP
TMP=/home/wschreye/scratch

python mergeTallies.py $TMP/*.root

#$MCNP_PATH/MCNP_CODE/bin/merge_mctal $TMP/tal*
#merge_meshtal $TMP/meshtal*
#mv $TMP/out1 out1
python writeREADME.py > README.md
./plot.sh
#rm slurm-*
#rm $TMP/out* $TMP/tal* $TMP/meshtal*
#param=$(grep 'He-II - heat exchanger:' README.md | cut -d ' ' -f 5)
#git add MCTALMRG MESHTALMRG README.md out1 ucn.inp ucn.mcnp
#git commit -m "Changed target offset to ${param}cm"
