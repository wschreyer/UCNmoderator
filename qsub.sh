#!/bin/sh

JOBID=$(qsub -d . -t 1-10 job.sh)
echo $JOBID
qsub -d . -W depend=afterokarray:$JOBID analyze.sh
