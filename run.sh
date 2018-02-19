#!/bin/sh

#SBATCH --time=20
#SBATCH --mem=2000M
#PBS -l walltime=00:20:00

echo "Running on `hostname`"
SCR=/home/wschreye/scratch
MCNP_PATH=/home/wschreye/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA

ID=$SLURM_ARRAY_TASK_ID$PBS_ARRAYID
TMP=$SLURM_TMPDIR$LSCRATCH

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > $TMP/ucn$ID.mcnp
rm -f ${TMP}/${ID}?
$MCNP_PATH/MCNP_CODE/bin/mcnp6 i=$TMP/ucn$ID.mcnp name=$TMP/$ID
rm -f $TMP/${ID}r $TMP/${ID}d $TMP/${ID}e $TMP/ucn$ID.mcnp
python /home/wschreye/UCNmoderator/readTallies.py ${TMP}/${ID}m $SCR/tallies${ID}.root
if [ $ID = "1" ]
then
  cp $TMP/${ID}o out1
fi
rm -f $TMP/${ID}o
