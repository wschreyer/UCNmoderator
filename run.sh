#!/bin/sh

#SBATCH --time=30
#SBATCH --mem=2000M
#PBS -l walltime=00:30:00

echo "Running on `hostname`"
MCNP_PATH=/home/wschreye/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA

ID=$SLURM_ARRAY_TASK_ID$PBS_ARRAYID
SCR=/home/wschreye/scratch
TMP=$SLURM_TMPDIR$LSCRATCH

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > $TMP/ucn$ID.mcnp
rm -f $TMP/${ID}?
$MCNP_PATH/MCNP_CODE/bin/mcnp6 i=$TMP/ucn$ID.mcnp name=$TMP/$ID
rm -f $TMP/${ID}r $TMP/${ID}d $TMP/${ID}e
python readTallies.py ${TMP}/${ID}m $SCR/tallies${ID}.root
mv $TMP/${ID}m $SCR/
if [ $ID = "1" ]
then
  cp $TMP/${ID}o out1
fi
rm -f $TMP/${ID}o
