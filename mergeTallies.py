import sys
import ROOT
import multiprocessing
import os

def mergeTallies(files):
  ohists = {}
  for fn in files:
    print(fn)
    ifile = ROOT.TFile(fn, 'READ')
    keys = ifile.GetListOfKeys()
#    print([k.GetName() for k in keys])
    for key in keys:
      tally = key.GetName()
      ihist = ifile.Get(tally)
      if tally in ohists:
        ohists[tally].Add(ihist)
      else:
        ohists[tally] = ihist
        ohists[tally].SetDirectory(0)
    ifile.Close()
    os.remove(fn)
  return ohists

threads = 8
pool = multiprocessing.Pool(processes = threads)
files = [sys.argv[i::threads] for i in range(1, threads + 1)]
histlist = pool.map(mergeTallies, files)
ohists = histlist[0]
for hists in histlist[1:]:
  for h in hists:
    ohists[h].Add(hists[h])
ofile = ROOT.TFile('tallies.root', 'RECREATE')
for h in ohists:
  ohists[h].Write(h)
ofile.Close()
