#!/bin/sh

#SBATCH --time=1
#SBATCH --mem=100M

rm -rf /home/wschreye/scratch/*
rm -rf tallies.root

python changeLD2contamination.py

