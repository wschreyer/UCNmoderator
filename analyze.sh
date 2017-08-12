#!/bin/sh

export FLUPRO=/home/wschreyer/fluka2011.2c-6

rm ranucn_*
rm job.sh.*
{ ls ucn_*_fort.21; echo ; echo ucn_21.trk; } | $FLUPRO/flutil/ustsuw
rm ucn_*_fort.21
{ ls ucn_*_fort.22; echo ; echo ucn_22.bnn; } | $FLUPRO/flutil/usbsuw
{ echo ucn_22.bnn; echo ucn_22.bnn.asc; } | $FLUPRO/flutil/usbrea
rm ucn_*_fort.22
{ ls ucn_*_fort.23; echo ; echo ucn_23.rnc; } | $FLUPRO/flutil/usrsuw
rm ucn_*_fort.23
{ ls ucn_*_fort.24; echo ; echo ucn_24.bnn; } | $FLUPRO/flutil/usbsuw
rm ucn_*_fort.24
head README.md -n16 > READMEn.md
python sum_flux_energy.py | tail -n27 >> READMEn.md
mv READMEn.md README.md
rm *.out
rm *.err
rm *.log
rm fort.11
git README.md add ucn.inp ucn.flair ucn_2*
