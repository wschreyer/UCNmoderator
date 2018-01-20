import re
import io
import math
import sys
import ROOT
import numpy
import fcntl

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'
minbin = {'f': 0, 'x': -sys.float_info.max, 'y': -sys.float_info.max, 'z': -sys.float_info.max, 'u': 0, 's': 0, 'm': 0, 'c': -1., 'e': 0., 't': 0}

def ReadTally(mctal):
  tally = {}
  line = '\n'
  while line.endswith('\n'):
    line = mctal.readline()
    match = re.match('tally\s+(\d+)', line)
    if match:
      tally['tally'] = int(match.group(1))
#      print('tally', tally['tally'])
      break
  else:
    return

  line = mctal.readline()
  while not line.startswith('vals'):
    match = re.match('([fcet])([tc])?\s+(\d+)', line)
    if match:
      bins = match.group(1)
      nbins = int(match.group(3))
      if bins == 'f' and nbins == 0: # add default f only if there is none given
        tally[bins] = [minbin[bins]]
      elif bins in ['c','e','t'] and 'x' in tally and nbins == 1: # TMESH tallies set 'c','e','t' all to 1
        tally[bins] = [minbin[bins]]
      elif bins in ['c','e','t']: # add min bin for all other bins
        nbins = nbins + 1
        tally[bins] = [minbin[bins]]
      else:
        tally[bins] = []
      extrabins = 0
      if match.group(2):
        extrabins = 1 # if 'e' or 't' are followed by 'c' or 't' vals contain an extra entry with the total of all bins

      match = re.findall('(\d+)', line)
      if len(match) == 1:
        line = mctal.readline()
        while not re.match('\S+', line):
          for m in re.findall(reg, line):
            if bins == 'f':
              tally[bins].append(int(m))
            else:
              tally[bins].append(float(m))
          line = mctal.readline()
        if extrabins == 1:
          tally[bins].append(float('inf')) # add extra bin entry if total is contained in vals
        if bins == 'f':
          for b in ['x','y','z']:
            tally[b] = [minbin[b]]
#        print(bins, nbins, tally[bins])
        assert(len(tally[bins]) == nbins)
      elif len(match) == 5 and bins == 'f': # handle TMESH tallies separately
        x = int(match[2])
        y = int(match[3])
        z = int(match[4])
        assert(nbins == x*y*z)
        tally['f'] = [minbin['f']]
        for b in ['x','y','z']:
          tally[b] = []
        line = mctal.readline()
        while not re.match('\S+', line):
          for m in re.findall(reg, line):
            if len(tally['x']) == x + 1 and len(tally['y']) == y + 1:
              tally['z'].append(float(m))
            elif len(tally['x']) == x + 1:
              tally['y'].append(float(m))
            else:
              tally['x'].append(float(m))
          line = mctal.readline()
        assert(len(tally['x']) == x + 1 and len(tally['y']) == y + 1 and len(tally['z']) == z + 1)
#        print('x',tally['x'])
#        print('y',tally['y'])
#        print('z',tally['z'])
      else:
        assert(False)
#      print(bins, nbins, tally[bins])
    else:
      line = mctal.readline()

  nvals = 1
  for b in tally:
    if b in ['x','y','z','c','e','t'] and len(tally[b]) > 1:
      nvals = nvals * (len(tally[b]) - 1)
    elif b == 'f':
      nvals = nvals * len(tally[b])
#  print('expect', nvals)

  tally['vals'] = []
  tally['errs'] = []
  fp = mctal.tell()
  line = mctal.readline()
  while line.endswith('\n') and not re.match('\S+', line):
    match = re.findall(reg, line)
    for i in range(len(match)/2):
      val = float(match[i*2])
      tally['vals'].append(val)
      tally['errs'].append(float(match[i*2 + 1])*val)
    fp = mctal.tell()
    line = mctal.readline()
#  print(nvals, len(tally['vals']), len(tally['errs']))
  assert(len(tally['vals']) == nvals and len(tally['errs']) == nvals)
  assert((not line.endswith('\n')) or line.startswith('tfc') or ('x' in tally and line.startswith('tally')))
#  print(tally)
  mctal.seek(fp)
  return tally
#enddef ReadTally

def ReadTallies(fn):
  print(fn)
  tallies = {}
  mctal = io.FileIO(fn)
  while True:
    tally = ReadTally(mctal)
    if tally:
      tallies[tally['tally']] = tally
    else:
      break
  return tallies
#enddef ReadTallies

def MergeTallies(tally1, tally2):
  for b in tally1:
    if b not in ['vals', 'errs']:
      assert(tally1[b] == tally2[b])
    else:
      assert(len(tally1[b]) == len(tally2[b]))
  for i in range(len(tally1['vals'])):
    v1 = tally1['vals'][i]
    v2 = tally2['vals'][i]
    if v2 == 0.:
      continue
    elif v1 == 0.:
      tally1['vals'][i] = v2
      tally1['errs'][i] = tally2['errs'][i]
    else:
      w1 = 1./tally1['errs'][i]**2
      w2 = 1./tally2['errs'][i]**2
      tally1['vals'][i] = (tally1['vals'][i]*w1 + tally2['vals'][i]*w2)/(w1 + w2)
      tally1['errs'][i] = math.sqrt(1./(w1 + w2))
  return tally1
#enddef MergeTallies

def Draw3DTally(tally, xb, yb, zb):
  hists = {}
  i = 0
  for b in tally:
    if b not in [xb,yb,zb,'tally','f','vals','errs']:
      assert(len(tally[b]) == 1)
  for f in tally['f']:
    name = 'tally{0}_cell{1}'.format(tally['tally'], f)
    xs = tally[xb]
    ys = tally[yb]
    zs = tally[zb]
    hists[f] = ROOT.TH3D(name, name, len(xs) - 1, numpy.array(xs), len(ys) - 1, numpy.array(ys), len(zs) - 1, numpy.array(zs))
    for x in xs[:-1]:
      for y in ys[:-1]:
        for z in zs[:-1]:
          b = hists[f].FindBin(x + 1, y + 1, z + 1)
          hists[f].SetBinContent(b, tally['vals'][i])
          hists[f].SetBinError(b, tally['errs'][i])
          i = i + 1
    hists[f].SetBit(ROOT.TH1.kIsAverage)
  return hists
#enddef Draw3DTally

def Draw2DTally(tally, xb, yb):
  hists = {}
  i = 0
  for b in tally:
    if b not in [xb,yb,'tally','f','vals','errs']:
      assert(len(tally[b]) == 1)
  for f in tally['f']:
    name = 'tally{0}_cell{1}'.format(tally['tally'], f)
    xs = tally[xb]
    ys = tally[yb]
    xtot = 0
    if xs[-1] == float('inf'):
      xtot = 1
    ytot = 0
    if ys[-1] == float('inf'):
      ytot = 1
    hists[f] = ROOT.TH2D(name, name, len(xs) - 1 - xtot, numpy.array(xs[:-xtot]), len(ys) - 1 - ytot, numpy.array(ys[:-ytot]))
    for x in xs[:-1]:
      for y in ys[:-1]:
        b = hists[f].FindBin(x,y)
        hists[f].SetBinContent(b, tally['vals'][i])
        hists[f].SetBinError(b, tally['errs'][i])
        i = i + 1
    hists[f].SetBit(ROOT.TH1.kIsAverage)
  return hists
#enddef Draw2DTally

def Draw1DTally(tally, xb):
  hists = {}
  i = 0
  for b in tally:
    if b not in [xb,'tally','f','vals','errs']:
      assert(len(tally[b]) == 1)
  for f in tally['f']:
    name = 'tally{0}_cell{1}'.format(tally['tally'], f)
    xs = tally[xb]
    if xs[-1] == float('inf'):
      hists[f] = ROOT.TH1D(name, name, len(xs) - 2, numpy.array(xs[:-1]))
    else:
      hists[f] = ROOT.TH1D(name, name, len(xs) - 1, numpy.array(xs))
    for x in xs[:-1]:
      b = hists[f].FindBin(x)
      hists[f].SetBinContent(b, tally['vals'][i])
      hists[f].SetBinError(b, tally['errs'][i])
      i = i + 1
    hists[f].SetBit(ROOT.TH1.kIsAverage)
  return hists
#enddef Draw1DTally

def Draw0DTally(tally):
  hists = {}
  assert(len(tally['f']) == len(tally['vals']))
  for b in tally:
    if b not in ['tally', 'f', 'vals', 'errs']:
      assert(len(tally[b]) == 1)
  name = 'tally{0}'.format(tally['tally'])
  fmin = min(tally['f'])
  fmax = max(tally['f'])
  hists[0] = ROOT.TH1D(name, name, fmax - fmin + 1, fmin - 0.5, fmax + 0.5)
  for f, val, err in zip(tally['f'], tally['vals'], tally['errs']):
    b = hists[0].FindBin(f)
    hists[0].SetBinContent(b, val)
    hists[0].SetBinError(b, err)
  hists[0].SetBit(ROOT.TH1.kIsAverage)
  return hists
#enddef Draw0DTally

def WriteTallies(hists):
  rootfile = ROOT.TFile(sys.argv[2], 'UPDATE')
  for h in hists:
    print(hists[h].GetName())
    hists[h].Write(hists[h].GetName())
  rootfile.Close()

tallies = ReadTallies(sys.argv[1])
for t in tallies:
  hists = {}
  if t in range(1,201,10) or t in [3]:
    hists = Draw3DTally(tallies[t], 'z', 'y', 'x')
  elif t in [4]:
    hists = Draw2DTally(tallies[4], 'e', 't')
  elif t in [116,76,86,96,106,124]:
    hists = Draw1DTally(tallies[t], 't')
  elif t in [14, 24, 64, 74, 84, 94, 134, 144]:
    hists = Draw0DTally(tallies[t])
  else:
    assert(True)
  WriteTallies(hists)

