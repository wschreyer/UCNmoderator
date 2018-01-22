#!/bin/sh

echo 'basis 1 0 0 0 0 1  origin 0 0 40  extent 100 70  &' > comout
echo 'label 0 0  color off  viewport square' >> comout
echo 'end' >> comout

MCNP_PATH=/home/wschreye/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA
module load root
module load python27-scipy-stack

$MCNP_PATH/MCNP_CODE/bin/mcnp6 ip i=ucn.mcnp com=comout notek

python plot.py

rm comout comouu outp plotm.ps mdata
