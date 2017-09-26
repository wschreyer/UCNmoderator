#!/bin/sh

#SBATCH --time=10
#SBATCH --mem=1000M

echo "Running on `hostname`"
MCNP_PATH=/home/wschreye/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA

ID=$SLURM_ARRAY_TASK_ID
TMP=/home/wschreye/scratch

rm -f $TMP/ucn_$ID.mcnp $TMP/out$ID $TMP/run$ID $TMP/tal$ID $TMP/meshtal$ID $TMP/mdata$ID
sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > $TMP/ucn_$ID.mcnp
$MCNP_PATH/MCNP_CODE/bin/mcnp6 inp=$TMP/ucn_$ID.mcnp outp=$TMP/out$ID runtpe=$TMP/run$ID mctal=$TMP/tal$ID meshtal=$TMP/meshtal$ID mdata=$TMP/mdata$ID
rm -f $TMP/ucn_$ID.mcnp
rm -f $TMP/run$ID
rm -f $TMP/mdata$ID
