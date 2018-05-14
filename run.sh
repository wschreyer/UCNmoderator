#!/bin/sh

#SBATCH --time=30
#SBATCH --nodes=1
###SBATCH --mem=2000M
###SBATCH --array=1-20

echo "Running on `hostname`"
MCNP_PATH=$SCRATCH/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA
TMP=${SCRATCH}/$1

mkdir $TMP
for i in `seq 40`; do
  sed -e "s/MYSEED/`date +%N`/g" $TMP/ucn.mcnp > $TMP/ucn$i.mcnp
done
parallel --lb "${MCNP_PATH}/MCNP_CODE/bin/mcnp6 i=${TMP}/ucn{}.mcnp name=${TMP}/{}; python readTallies.py ${TMP}/{}m" ::: `seq 40`
python mergeTallies.py ${TMP}/*m.root ${TMP}/tallies.root
cp $TMP/1o ${TMP}/out1
rm ${TMP}/{1..40}?
rm ${TMP}/ucn{1..40}.mcnp
python writeREADME.py ${TMP}/out1 ${TMP}/tallies.root > ${TMP}/README.md
