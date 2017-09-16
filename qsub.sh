#!/bin/sh

if [ $# -gt 0 ]
then
  JOBID=$(qsub -cwd -hold_jid $1 prerun.sh | cut -f 3 -d " ")
else
  JOBID=$(qsub -cwd prerun.sh | cut -f 3 -d " ")
fi
echo $JOBID

JOBID=$(qsub -cwd -hold_jid $JOBID -t 1-250 run.sh | cut -f 3 -d " " | cut -f 1 -d ".")
echo $JOBID

qsub -cwd -hold_jid $JOBID postrun.sh

