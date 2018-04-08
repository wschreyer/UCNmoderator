#!/bin/sh

#SBATCH --time=60
#SBATCH --mem=2000M
#SBATCH --array=1-20

echo "Running on `hostname`"
SCR=/home/wschreye/scratch
MCNP_PATH=/home/wschreye/scratch/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA

ID=$SLURM_ARRAY_JOB_ID$SLURM_ARRAY_TASK_ID
TMP=$SLURM_TMPDIR

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > $TMP/ucn$ID.mcnp
rm -f ${TMP}/${ID}?
time $MCNP_PATH/MCNP_CODE/bin/mcnp6 i=$TMP/ucn$ID.mcnp name=$TMP/$ID
rm -f $TMP/${ID}r $TMP/${ID}d $TMP/${ID}e $TMP/ucn$ID.mcnp
time python /home/wschreye/UCNmoderator/readTallies.py ${TMP}/${ID}m tallies${ID}.root
if [ $SLURM_ARRAY_TASK_ID = "1" ]
then
  cp $TMP/${ID}o out1
fi
rm -f $TMP/${ID}o
