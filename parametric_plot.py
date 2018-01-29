import ROOT
import io
import subprocess
import sys
import math
import os

pname = 'Configuration'

### get parameter from cells
def GetParameter(cells):
  return cells

#ROOT.TGaxis.SetMaxDigits(2)
ROOT.gStyle.SetMarkerStyle(21)
history = int(sys.argv[1])
grUCN = ROOT.TGraphErrors(history)
grUCN.SetFillStyle(0)
grUCNperHeat = ROOT.TGraphErrors(history)
ROOT.gStyle.SetMarkerColor(ROOT.kRed)
gpHe = ROOT.TGraphErrors(history)
gpHe.SetFillStyle(0)
gdHe = ROOT.TGraphErrors(history)
gdHe.SetFillStyle(0)
gdHe.SetMarkerStyle(22)
ROOT.gStyle.SetMarkerColor(ROOT.kGreen)
gpBtl = ROOT.TGraphErrors(history)
gpBtl.SetFillStyle(0)
gdBtl = ROOT.TGraphErrors(history)
gdBtl.SetFillStyle(0)
gdBtl.SetMarkerStyle(22)
sys.dont_write_bytecode = True
for i in range(0, history):
  git = 'HEAD~{0:d}:'.format(i)
  reader = open('tmp.py', 'w')
  subprocess.call(['git', 'show', git + 'readResults.py'], stdout=reader)
  reader.close()
  import tmp as readResults
  reload(readResults)
  out = subprocess.check_output(['git', 'show', git + 'out1'])
  cells = readResults.ReadCells(io.StringIO(unicode(out)))
  surfaces = readResults.ReadSurfaces(io.StringIO(unicode(out)))
  tallies = open('tmp.root','w')
  subprocess.call(['git', 'show', git + 'tallies.root'], stdout=tallies)
  tallies.close()
  tallies = ROOT.TFile('tmp.root', 'READ')

  p = history - i#GetParameter(cells)
  UCN = readResults.GetUCNProduction(tallies)
#  print '{0:.3g} +- {1:.2g}'.format(UCN[0], UCN[1])

  pHe = readResults.GetPromptHeat(tallies, readResults.HeIIcell)
  pBtl= readResults.GetPromptHeat(tallies, readResults.HeIIbottlecell)
  dHe = readResults.GetMaxDelayedHeat(tallies, readResults.HeIIcell)
  dBtl= readResults.GetMaxDelayedHeat(tallies, readResults.HeIIbottlecell)
  heat = pHe[0] + pBtl[0] + dHe[0] + dBtl[0]  
  dheat = math.sqrt(pHe[1]**2 + pBtl[1]**2 + dHe[1]**2 + dBtl[1]**2)

  grUCN.SetPoint(i, p, UCN[0]/1e4)
  grUCN.SetPointError(i, 0, UCN[1]/1e4)
  grUCNperHeat.SetPoint(i, p, UCN[0]/1e4/heat)
  grUCNperHeat.SetPointError(i, 0, math.sqrt((UCN[1]/1e4/heat)**2 + (dheat*UCN[0]/1e4/heat**2)**2))
  gpHe.SetPoint(i, p, pHe[0])
  gpHe.SetPointError(i, 0, pHe[1])
  gpBtl.SetPoint(i, p, pBtl[0])
  gpBtl.SetPointError(i, 0, pBtl[1])
  gdHe.SetPoint(i, p, dHe[0])
  gdHe.SetPointError(i, 0, dHe[1])
  gdBtl.SetPoint(i, p, dBtl[0])
  gdBtl.SetPointError(i, 0, dBtl[1])

  tallies.Close()
  os.remove('tmp.root')
  os.remove('tmp.py')

c2 = ROOT.TCanvas('c2', 'c2', 800, 600)
leg = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
mg = ROOT.TMultiGraph()
mg.Add(grUCN)
leg.AddEntry(grUCN, 'UCN production')
mg.Add(gpHe)
leg.AddEntry(gpHe, 'Prompt heat He-II')
mg.Add(gpBtl)
leg.AddEntry(gpBtl, 'Prompt heat He bottle')
mg.Add(gdHe)
leg.AddEntry(gdHe, 'Delayed heat He-II')
mg.Add(gdBtl)
leg.AddEntry(gdBtl, 'Delayed heat He bottle')
mg.SetMinimum(0)
mg.Draw("AP")
mg.GetXaxis().SetTitle(pname)
mg.GetYaxis().SetTitle('UCN production (10^{4} s^{-1} #muA^{-1}) | Heat (mW #muA^{-1})')
mg.Draw("AP")
leg.Draw()
c2.Print('UCNandHeat.pdf')

c3 = ROOT.TCanvas('c3', 'c3', 800, 600)
grUCNperHeat.SetMinimum(0)
grUCNperHeat.SetTitle('')
grUCNperHeat.GetXaxis().SetTitle(pname)
grUCNperHeat.GetYaxis().SetTitle('UCN production per heat (10^{4} s^{-1} mW^{-1})')
grUCNperHeat.Draw('AP')
c3.Print('UCNperHeat.pdf')

