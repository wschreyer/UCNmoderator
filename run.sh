#!/bin/sh

#SBATCH --time=120
#SBATCH --nodes=1
#SBATCH --array=1-100

echo "Running on `hostname`"
MCNP_PATH=/nedm1/nedm/w78
export DATAPATH=$MCNP_PATH/MCNP_DATA/MCNP_DATA
ID=$SLURM_ARRAY_JOB_ID/$SLURM_ARRAY_TASK_ID

mkdir $MCNP_PATH/UCNmoderator/$SLURM_ARRAY_JOB_ID
TMP=$MCNP_PATH/UCNmoderator/$ID
sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > ${TMP}ucn.mcnp
mcnp6 i=${TMP}ucn.mcnp name=$ID
python readTallies.py ${TMP}m
