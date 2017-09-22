#!/bin/sh

#SBATCH --time=30
#SBATCH --mem=1000M

echo "Running on `hostname`"
MCNP_PATH=/home/wschreye/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA

ID=$SLURM_ARRAY_TASK_ID
TMP=/tmp

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > ucn_$ID.mcnp
rm -f out$ID $TMP/run$ID tal$ID meshtal$ID $TMP/mdata$ID
$MCNP_PATH/MCNP_CODE/bin/mcnp6 inp=ucn_$ID.mcnp outp=out$ID runtpe=$TMP/run$ID mctal=tal$ID meshtal=meshtal$ID mdata=$TMP/mdata$ID
rm -f ucn_$ID.mcnp
rm -f $TMP/run$ID
rm -f $TMP/mdata$ID
