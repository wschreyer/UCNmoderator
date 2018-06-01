import ROOT
import io
import re
import numpy
import readResults
import math

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'

def DrawGeometry(lv, zmax):
  xmin = 9e99
  xmax = -9e99
  ymin = 9e99
  ymax = -9e99
  for l in lv:
    xmin = min([xmin, l[0], l[2]])
    xmax = max([xmax, l[0], l[2]])
    ymin = min([ymin, l[1], l[3]])
    ymax = max([ymax, l[1], l[3]])
  xscale = 450./(xmax - xmin)
  yscale = (zmax + 30.)/(ymax - ymin)
  lines = []
  for l in lv:
    lines.append(ROOT.TLine((l[0] - xmin)*xscale - 300., (l[1] - ymin)*yscale - 30., (l[2] - xmin)*xscale - 300., (l[3] - ymin)*yscale - 30.))
    lines[-1].Draw()
  return lines


def DrawPlot(gr, canvas, title):
  canvas.SetRightMargin(0.12)
  canvas.SetLogz()
  gr.SetTitle(title)
  gr.GetXaxis().SetTitle("y (cm)")
  gr.GetYaxis().SetTitle("z (cm)")
  gr.GetZaxis().SetRangeUser(1e-7, 1e-5)
  gr.SetStats(0)
  gr.Draw("COL1Z")

ROOT.gROOT.SetBatch(True)
tallies = ROOT.TFile('tallies.root', 'READ')

f = io.open("plotm.ps")
lv = []
for line in f:
  match = re.match(reg+reg+'\s+(moveto)'+reg+reg+'\s+(lineto)', line)
  if match:
    lv.append([float(m) for m in match.group(1,2,4,5)])
f.close()

f = io.open("ucn.mcnp")
zmax = -9e99
for line in f:
  match = re.match('\s*([+-]?\d+)\s+(\S+)'+reg+reg+reg+reg+reg+reg, line)
  if match:
    if match.group(1) == '113':
      assert(match.group(2) == 'RPP')
      zmax = float(match.group(8))
      break
print 'zmax = {0}'.format(zmax)
assert(zmax != -9e99)

c20 = ROOT.TCanvas("c20", "c20", 800, 600)
DrawPlot(tallies.Get('tally101_cell0').Project3D('zy'), c20, 'Neutron flux <6 meV')
lines = DrawGeometry(lv, zmax)
c20.Print("n20K.pdf")

c300 = ROOT.TCanvas("c300", "c300", 800, 600)
DrawPlot(tallies.Get('tally111_cell0').Project3D('zy'), c300, 'Neutron flux 6-100 meV')
lines = DrawGeometry(lv, zmax)
c300.Print("n300K.pdf")

cfast = ROOT.TCanvas("cfast", "cfast", 800, 600)
cfast.SetLogy()
DrawPlot(tallies.Get('tally121_cell0').Project3D('zy'), cfast, 'Neutron flux >100 meV')
lines = DrawGeometry(lv, zmax)
cfast.Print("nfast.pdf")

cdep = ROOT.TCanvas('cdep', 'cdep', 800, 600)
DrawPlot(tallies.Get('tally3_cell0').Project3D('zy'), cdep, 'Heat deposition')
lines = DrawGeometry(lv, zmax)
cdep.Print('Edep.pdf')

cgheat = ROOT.TCanvas('cgheat', 'cgheat', 800, 600)
hgheat = tallies.Get('tally13_cell0').ProjectionY('_py', 2)
hgheat.Scale(40.*14.42*1000.)
hgheat.SetTitle('Heat deposited in guide wall (125x3mm Al @ 40uA)')
hgheat.GetXaxis().SetTitle('Horizontal distance from target (cm)')
hgheat.GetYaxis().SetTitle('Deposited energy (mW/cm)')
hgheat.SetStats(0)
hgheat.Draw()
cgheat.Print('gheat.pdf')

#ROOT.TGaxis.SetMaxDigits(2)
cspec = ROOT.TCanvas("cspec", "cspec", 800, 600)
cspec.SetLogx()
cspec.SetLogy()
hist = tallies.Get('tally4_cell19').ProjectionX()
hist.Scale(6.2415e12)
hist.GetXaxis().SetTitle('Energy (MeV)')
hist.GetYaxis().SetTitle('Flux (cm^{-2} s^{-1} #muA^{-1})')
hist.SetStats(0)
#hist.GetYaxis().SetRangeUser(1e5, 3e9)
hist.Draw('')
cspec.Print('spectrum.pdf')

ct = ROOT.TCanvas('ctime', 'ctime', 800, 600)
hist = tallies.Get('tally4_cell19')
b20 = hist.GetXaxis().FindBin(6e-9)
t20 = hist.ProjectionY('_20', 0, b20)
b300 = hist.GetXaxis().FindBin(100e-9) 
t300 = hist.ProjectionY('_300', b20 + 1, b300)
tfast = hist.ProjectionY('_fast', b300 + 1)
t300.SetTitle('Neutron flux <6 meV, 6-100 meV')
t300.SetLineColor(ROOT.kGreen)
tfast.SetLineColor(ROOT.kRed)
t300.GetXaxis().SetTitle('Time (shakes)')
t300.GetXaxis().SetRangeUser(0,1e6)
t300.GetYaxis().SetTitle('Flux per primary proton (cm^{-2})')
t300.SetStats(0)
t300.Draw('')
t20.Draw('SAME')
ct.Print('time.pdf')

cheat = ROOT.TCanvas('cheat', 'cheat', 800, 600)
heats = ROOT.THStack('heat', 'heat')
maxcell = 0
for t in tallies.GetListOfKeys():
  match = re.match('tally116_cell(\d+)', t.GetName())
  if match and int(match.group(1)) > maxcell:
    maxcell = int(match.group(1))
assert(maxcell > 0)
for t,p in zip([76, 96, 106, 86, 116], ['n', 'e', 'p', '#gamma', 'total']):
  hist = ROOT.TH1D(p, p, maxcell, 0.5, maxcell + 0.5)
  histd = ROOT.TH1D('delayed '+p, 'delayed '+p, maxcell, 0.5, maxcell + 0.5)
  for c in range(1, maxcell + 1):
    hist.Fill(c, readResults.GetPromptHeat(tallies, c, t)[0])
    histd.Fill(c, readResults.GetMaxDelayedHeat(tallies, c, t)[0])
  if t == 116:
#    ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)
    heats.Draw('pfc HIST')
    heats.SetMaximum(100)
    heats.Draw('pfc HIST')
    hist.Add(histd)
    hist.SetLineColor(ROOT.kRed)
    hist.Draw('SAMEHIST')
  else:
    heats.Add(hist)
    heats.Add(histd)
cheat.BuildLegend(0.5,0.7,0.8,0.85)
cheat.Print('heat.pdf')

