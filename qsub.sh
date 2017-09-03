#!/bin/sh

JOBID=$(qsub -d . -W depend=afterok:$1 prerun.sh)
echo $JOBID
JOBID=$(qsub -d . -W depend=afterok:$JOBID -t 1-100 run.sh)
echo $JOBID
qsub -d . -W depend=afterokarray:$JOBID postrun.sh

