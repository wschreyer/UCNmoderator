import ROOT
import io
import subprocess
import sys
import math
import readResults

ROOT.gROOT.SetBatch(True)

import parametric_plot

pname = parametric_plot.pname

### get parameter from cells
def GetParameter(surfaces):
  return parametric_plot.GetParameter(surfaces)

ROOT.TGaxis.SetMaxDigits(3)
ROOT.gStyle.SetMarkerColor(ROOT.kBlack)
ROOT.gStyle.SetMarkerStyle(21)
history = int(sys.argv[1])

gr = ROOT.TGraphErrors(history)

gtaumax = ROOT.TGraphErrors(history)
gtaumin = ROOT.TGraphErrors(history)
gtaumin.SetMarkerColor(ROOT.kRed)
gtauwalldom = ROOT.TGraphErrors(history)
gtauwalldom.SetMarkerColor(ROOT.kGreen)
gtauhedom = ROOT.TGraphErrors(history)
gtauhedom.SetMarkerColor(ROOT.kBlue)

gheat = {}

grUCN = ROOT.TGraphErrors(history)
grUCN.SetFillStyle(0)
for i in range(0, history):
  git = 'HEAD~{0:d}:'.format(i)
  out = subprocess.check_output(['git', 'show', git + 'out1'])
  cells = readResults.ReadCells(io.StringIO(unicode(out)))
  surfaces = readResults.ReadSurfaces(io.StringIO(unicode(out)))
  tal = subprocess.check_output(['git', 'show', git + 'MCTALMRG'])
  tallies = readResults.ReadTallies(io.StringIO(unicode(tal)))

  p = GetParameter(surfaces)
  UCN = readResults.GetUCNProduction(tallies, cells, 14)
#  print '{0:.3g} +- {1:.2g}'.format(UCN[0], UCN[1])

  for cell in tallies[116]['cells']:
    if not cell in gheat:
      gheat[cell] = ROOT.TGraphErrors(history)
      gheat[cell].SetFillStyle(0)
    pheat = readResults.GetPromptHeat(tallies, cells, cell)
    dheat = readResults.GetMaxDelayedHeat(tallies, cells, cell)
    gheat[cell].SetPoint(i, p, (pheat[0] + dheat[0])*1000)
    gheat[cell].SetPointError(i, 0, math.sqrt(pheat[1]**2 + dheat[1]**2)*1000)

  pHe = readResults.GetPromptHeat(tallies, cells, 14)
  pBtl= readResults.GetPromptHeat(tallies, cells, 13)
  dHe = readResults.GetMaxDelayedHeat(tallies, cells, 14)
  dBtl= readResults.GetMaxDelayedHeat(tallies, cells, 13)
  heat = pHe[0] + pBtl[0] + dHe[0] + dBtl[0]  
  dheat = math.sqrt(pHe[1]**2 + pBtl[1]**2 + dHe[1]**2 + dBtl[1]**2)

  gr.SetPoint(i, p, UCN[0]/heat)
  gr.SetPointError(i, 0, math.sqrt((UCN[1]/UCN[0])**2 + (dheat/heat)**2)*UCN[0]/heat)

  tauupmax = 2870.*(heat*40.)**-1.42
  tauupmean = 1654.*(heat*40.)**-1.31
  tauupmin = 616*(heat*40.)**-1.22
  tauwall = 39.2*cells[14]['volume']/(surfaces[36]['area'] + surfaces[42]['area'] - surfaces[42]['size'][6]**2*math.pi*2)
  print(tauwall)
  taumax = 1./(1./tauupmax + 1./880. + 1./tauwall)
  tauwalldom = 1./(1./tauupmax + 1./880. + 2./tauwall)
  tauhedom = 1./(1./tauupmin + 1./880. + 1./tauwall)
  taumin = 1./(1./tauupmin + 1./880. + 2./tauwall)

  gtaumax.SetPoint(i, p, UCN[0]*40.*taumax)
  gtauwalldom.SetPoint(i, p, UCN[0]*40.*tauwalldom)
  gtauhedom.SetPoint(i, p, UCN[0]*40.*tauhedom)
  gtaumin.SetPoint(i, p, UCN[0]*40.*taumin)
  #gr.SetPointError(i, 0, 0, maxval - meanval, meanval - minval)

  grUCN.SetPoint(i, p, UCN[0]/1e4)
  grUCN.SetPointError(i, 0, UCN[1]/1e4)

c0 = ROOT.TCanvas('c0','c0',800,600)
gr.SetMinimum(0)
gr.SetTitle("")
gr.GetXaxis().SetTitle(pname)
gr.GetYaxis().SetTitle('UCN production per heat (s^{-1} W^{-1})')
gr.Draw('AP')
c0.Print('UCNperHeat.pdf')

c1 = ROOT.TCanvas('c1','c1',800,600)
l = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
m = ROOT.TMultiGraph()
m.Add(gtaumax)
l.AddEntry(gtaumax, 'good cooling, low wall loss')
m.Add(gtaumin)
l.AddEntry(gtaumin, 'bad cooling, high wall loss')
m.Add(gtauwalldom)
l.AddEntry(gtauwalldom, 'good cooling, high wall loss')
m.Add(gtauhedom)
l.AddEntry(gtauhedom, 'bad cooling, low wall loss')
m.SetMinimum(0)
m.SetTitle("")
m.Draw('A')
m.GetXaxis().SetTitle(pname)
m.GetYaxis().SetTitle('UCN production #upoint lifetime')
m.Draw('AP')
l.Draw()
c1.Print('UCNtimesLifetime.pdf')

c2 = ROOT.TCanvas('c2', 'c2', 800, 600)
leg = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
mg = ROOT.TMultiGraph()
mg.Add(grUCN)
leg.AddEntry(grUCN, 'UCN production')
for cell, name in zip([14, 13, 22, 23], ['heat He-II', 'heat He bottle', 'heat heat exchanger', 'heat 3He']):
  mg.Add(gheat[cell])
  leg.AddEntry(gheat[cell], name)
mg.SetMinimum(0)
mg.Draw("AP")
mg.GetXaxis().SetTitle(pname)
mg.GetYaxis().SetTitle('UCN production (10^{4} s^{-1} #muA^{-1}) | Heat (mW #muA^{-1})')
mg.Draw("AP pmc plc")
leg.Draw()
c2.Print('UCNandHeat.pdf')

