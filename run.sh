#!/bin/sh

#SBATCH --time=12
#SBATCH --mem=2000M

echo "Running on `hostname`"
MCNP_PATH=/home/wschreye/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA

ID=$SLURM_ARRAY_TASK_ID
SCR=/home/wschreye/scratch
TMP=$SLURM_TMPDIR

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > $TMP/ucn$ID.mcnp
$MCNP_PATH/MCNP_CODE/bin/mcnp6 i=$TMP/ucn$ID.mcnp name=$TMP/$ID
rm -f $TMP/${ID}r $TMP/${ID}d $TMP/${ID}e
python readTallies.py ${TMP}/${ID}m $SCR/tallies${ID}.root
mv $TMP/${ID}m $SCR/
if [ $ID = "1" ]
then
  cp $TMP/${ID}o out1
fi
rm -f $TMP/${ID}o
