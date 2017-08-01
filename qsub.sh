#!/bin/sh

run=1

while [ $run -le 500 ]
do
sed -e "s/MYSEED/`date +%N | tail -c 6`./g" ucn.inp > ~/scratch/flukasims/fluka_$run.inp
sed -e "s/RUN/${run}/g" job.sh > ~/scratch/flukasims/job_$run.sh

cd ~/scratch/flukasims/
chmod 777 job_$run.sh
qsub job_$run.sh
cd -

run=`expr $run + 1`

done
