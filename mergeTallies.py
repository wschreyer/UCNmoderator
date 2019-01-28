import sys
import ROOT
import multiprocessing
import os

def mergeTallies(files):
  ohists = {}
  counts = {}
  for fn in files:
    print(fn)
    ifile = ROOT.TFile(fn, 'READ')
    keys = ifile.GetListOfKeys()
#    print([k.GetName() for k in keys])
    for key in keys:
      tally = key.GetName()
      ihist = ifile.Get(tally)
      ihist.SetBit(ihist.kIsAverage, False)
      if tally in ohists:
        assert(ohists[tally].Add(ihist))
        counts[tally] = counts[tally] + 1
      else:
        ohists[tally] = ihist
        counts[tally] = 1
        ohists[tally].SetDirectory(0)
    ifile.Close()
#    os.remove(fn)
  for h in ohists:
    ohists[h].Scale(1./counts[h])
  return ohists

threads = 40
pool = multiprocessing.Pool(processes = threads)
files = [sys.argv[i:-1:threads] for i in range(1, threads + 1)]
ohists = {}
counts = {}
for hists in pool.imap_unordered(mergeTallies, files):
  if len(ohists) == 0:
    ohists = hists
    for h in ohists:
      counts[h] = 1
  else:
    for h in hists:
      assert(ohists[h].Add(hists[h]))
      counts[h] = counts[h] + 1
ofile = ROOT.TFile(sys.argv[-1], 'RECREATE')
for h in ohists:
  ohists[h].Scale(1./counts[h])
  ohists[h].Write()
ofile.Close()
