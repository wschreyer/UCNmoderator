#!/bin/sh

echo 'basis 0 1 0 0 0 1  origin 0 -100 175  extent 250 225  &' > comout
echo 'label 0 0  color off  viewport square' >> comout
echo 'end' >> comout

MCNP_PATH=/home/wschreye/scratch/MCNP
export DATAPATH=$MCNP_PATH/MCNP_DATA

$MCNP_PATH/MCNP_CODE/bin/mcnp6 ip i=ucn.mcnp com=comout notek

python plot.py

rm comout comouu outp plotm.ps mdata
