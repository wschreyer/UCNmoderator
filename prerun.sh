#!/bin/sh

#SBATCH --time=1
#SBATCH --mem=100M
#PBS -l walltime=00:01:00

rm -rf /home/wschreye/scratch/*
rm -rf tallies.root

#python changeHEXdistance.py

