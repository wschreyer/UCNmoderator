#!/bin/sh

if [ $# -gt 0 ]
then
  JOBID=$(sbatch -D . -d afterok:$1 prerun.sh | cut -f 4 -d " ")
else
  JOBID=$(sbatch -D . prerun.sh | cut -f 4 -d " ")
fi
echo $JOBID

JOBID=$(sbatch -D . -d afterok:$JOBID -a 1-500 run.sh | cut -f 4 -d " ")
echo $JOBID

sbatch -D . -d afterok:$JOBID postrun.sh

