import ROOT
import io
import subprocess
import sys
import math
import readResults

pname = 'Lead thickness (cm)'

### get parameter from cells
def GetParameter(cells):
  return float(cells[19]['size'][2]) - float(cells[15]['size'][5]) # return lead thickness

ROOT.gStyle.SetMarkerStyle(21)
history = int(sys.argv[1])
gr = ROOT.TGraphErrors(history)
grUCN = ROOT.TGraphErrors(history)
grUCN.SetFillStyle(0)
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
for i in range(0, history):
  git = 'HEAD~{0:d}:'.format(i)
  out = subprocess.check_output(['git', 'show', git + 'out1'])
  cells = readResults.ReadCells(io.StringIO(unicode(out)))
  tal = subprocess.check_output(['git', 'show', git + 'MCTALMRG'])
  tallies = readResults.ReadTallies(io.StringIO(unicode(tal)))

  p = GetParameter(cells)
  UCN = readResults.GetUCNProduction(tallies, cells, 14)
#  print '{0:.3g} +- {1:.2g}'.format(UCN[0], UCN[1])

  pHe = readResults.GetPromptHeat(tallies, cells, 14)
  pBtl= readResults.GetPromptHeat(tallies, cells, 13)
  dHe = readResults.GetMaxDelayedHeat(tallies, cells, 14)
  dBtl= readResults.GetMaxDelayedHeat(tallies, cells, 13)
  heat = pHe[0] + pBtl[0] + dHe[0] + dBtl[0]  
  dheat = math.sqrt(pHe[1]**2 + pBtl[1]**2 + dHe[1]**2 + dBtl[1]**2)

  gr.SetPoint(i, p, UCN[0]/heat)
  gr.SetPointError(i, 0, math.sqrt((UCN[1]/UCN[0])**2 + (dheat/heat)**2)*UCN[0]/heat)

  grUCN.SetPoint(i, p, UCN[0])
  grUCN.SetPointError(i, 0, UCN[1])
  gpHe.SetPoint(i, p, pHe[0])
  gpHe.SetPointError(i, 0, pHe[1])
  gpBtl.SetPoint(i, p, pBtl[0])
  gpBtl.SetPointError(i, 0, pBtl[1])
  gdHe.SetPoint(i, p, dHe[0])
  gdHe.SetPointError(i, 0, dHe[1])
  gdBtl.SetPoint(i, p, dBtl[0])
  gdBtl.SetPointError(i, 0, dBtl[1])

c1 = ROOT.TCanvas('c1','c1',800,600)
gr.SetMinimum(0)
gr.SetTitle("")
gr.GetXaxis().SetTitle(pname)
gr.GetYaxis().SetTitle('UCN production per heat (10^{4} s^{-1} mW^{-1})')
gr.Draw('AP')
c1.Print('UCNperHeat.pdf')

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
