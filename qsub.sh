#!/bin/sh

JOBID=$(qsub -d . -t 1-16 job.sh)
echo $JOBID
qsub -d . -W depend=afterokarray:$JOBID -F "$1" analyze.sh
