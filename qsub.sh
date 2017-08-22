#!/bin/sh

JOBID=$(qsub -d . -W depend=afterok:$1 prerun.sh)
echo $JOBID
JOBID=$(qsub -d . -W depend=afterok:$JOBID -t 1-16 run.sh)
echo $JOBID
qsub -d . -W depend=afterokarray:$JOBID -F "$1" postrun.sh
