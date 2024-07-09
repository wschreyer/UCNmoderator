#!/bin/sh

#SBATCH --time=5
#SBATCH --mem=2000M

python mergeTallies.py $1/*.root tallies.root
cp $1/1o out1
python writeREADME.py out1 tallies.root > README.md
#./plot.sh
