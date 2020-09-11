#!/bin/sh

#SBATCH --time=240
#SBATCH --mem=1000M
#SBATCH --account=rrg-rpicker

echo "Running on `hostname`"
SCR=$SCRATCH/flukasims
export FLUPRO=/home/wschreye/fluka

ID=$SLURM_ARRAY_TASK_ID$PBS_ARRAYID
TMP=$SLURM_TMPDIR$LSCRATCH
WD=${SCRATCH}/UCNmoderator

sed -e "s/MYSEED/`date +%N | head -c 6`/g" ucn.inp > $TMP/ucn$ID.inp
cd ${SCR}
time $FLUPRO/flutil/rfluka -N0 -M1 -e ${WD}/myfluka $TMP/ucn$ID
rm -f $TMP/ucn$ID.inp
