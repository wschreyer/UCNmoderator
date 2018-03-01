#!/bin/sh

#SBATCH --time=240
#SBATCH --mem=1000M
#PBS -l walltime=4:00:00

echo "Running on `hostname`"
SCR=/home/wschreye/scratch/flukasims

ID=$SLURM_ARRAY_TASK_ID$PBS_ARRAYID
TMP=$SLURM_TMPDIR$LSCRATCH
WD=${HOME}/UCNmoderator1

sed -e "s/MYSEED/`date +%N | head -c 6`/g" ucn.inp > $TMP/ucn$ID.inp
cd ${SCR}
time $FLUPRO/flutil/rfluka -N0 -M1 -e ${WD}/myfluka $TMP/ucn$ID
rm -f $TMP/ucn$ID.inp
