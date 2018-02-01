#!/bin/sh

if [ $# -gt 0 ]
then
  JOBID=$(qsub -d . -W depend=afterany:$1 prerun.sh | cut -f 1 -d ".")
  echo $JOBID
  JOBID=$(qsub -d . -W depend=afterok:$JOBID -t 1-100 run.sh | cut -f 1 -d ".")
else
  ./prerun.sh
  JOBID=$(qsub -d . -t 1-100 run.sh | cut -f 1 -d ".")
fi

echo $JOBID

qsub -d . -W depend=afterany:$JOBID postrun.sh

