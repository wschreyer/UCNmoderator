#!/bin/sh

#$ -l short=TRUE
#$ -l h_pmem=1000M

echo "Running on `hostname`"
MCNP_PATH=/nfs/mds/tmp/no72lum/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA

ID=$SGE_TASK_ID
TMP=/tmp

sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > ucn_$ID.mcnp
rm -f out$ID $TMP/run$ID tal$ID meshtal$ID $TMP/mdata$ID
$MCNP_PATH/MCNP_CODE/bin/mcnp6 inp=ucn_$ID.mcnp outp=out$ID runtpe=$TMP/run$ID mctal=tal$ID meshtal=meshtal$ID mdata=$TMP/mdata$ID
rm ucn_$ID.mcnp
rm $TMP/run$ID
rm $TMP/mdata$ID
