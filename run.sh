#!/bin/sh

#SBATCH --time=30
#SBATCH --nodes=1
#SBATCH --cpus-per-task=40

echo "Running on `hostname`"
MCNP_PATH=$SCRATCH/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA
SCR=$SCRATCH

for i in `seq 40`; do
  sed -e "s/MYSEED/`date +%N`/g" ucn.mcnp > $SCR/ucn$i.mcnp
done
parallel --lb "$MCNP_PATH/MCNP_CODE/bin/mcnp6 i=$SCR/ucn{}.mcnp name=$SCR/{}; python readTallies.py $SCR/{}m" ::: `seq 40`
python mergeTallies.py $SCR/*m.root $SCR/tallies.root
cp $SCR/1o $SCR/out1
rm -f $SCR/{1..40}?
rm -f $SCR/{1..40}m.root
rm -f $SCR/ucn{1..40}.mcnp
python writeREADME.py $SCR/out1 $SCR/tallies.root > $SCR/README.md
