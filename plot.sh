#!/bin/sh

echo 'basis 1 0 0 0 0 1  origin 0 0 40  extent 100 70  &' > comout
echo 'label 0 0  color off  viewport square' >> comout
echo 'end' >> comout

mcnp6 ip i=ucn.mcnp com=comout notek

root -l plot.cpp -q

rm comout comouu outp plotm.ps
