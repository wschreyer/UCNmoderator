#!/bin/sh

module load gcc/8.3.0
export FLUPRO=$HOME/fluka
export FLUFOR=gfortran
rm -f fluscw.o
rm -f usimbs.o
$FLUPRO/flutil/fff fluscw.f
$FLUPRO/flutil/fff usimbs.f
rm -f myfluka.map myfluka
$FLUPRO/flutil/lfluka -o myfluka -m fluka fluscw.o usimbs.o
