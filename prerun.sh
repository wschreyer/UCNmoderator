#!/bin/sh

#SBATCH --time=1
#SBATCH --mem=100M

rm -rf /home/wschreye/scratch/*
rm -rf tallies.root

python changeD2Oradius.py

