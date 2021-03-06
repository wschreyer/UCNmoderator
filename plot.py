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
  xscale = 200./(xmax - xmin)
  yscale = (zmax + 30.)/(ymax - ymin)
  lines = []
  for l in lv:
    lines.append(ROOT.TLine((l[0] - xmin)*xscale - 100., (l[1] - ymin)*yscale - 30., (l[2] - xmin)*xscale - 100., (l[3] - ymin)*yscale - 30.))
    lines[-1].Draw()
  return lines


def DrawPlot(gr, title):
  gr.SetTitle(title)
  gr.GetXaxis().SetTitle("x (cm)")
  gr.GetXaxis().SetLimits(-100.,100.)
  gr.GetYaxis().SetTitle("z (cm)")
  gr.GetYaxis().SetLimits(-30.,110.)
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
    if match.group(1) == '54':
      assert(match.group(2) == 'RPP')
      zmax = float(match.group(8))
      break
assert(zmax != -9e99)

c20 = ROOT.TCanvas("c20", "c20", 800, 600)
c20.SetRightMargin(0.12)
DrawPlot(tallies.Get('tally101_cell0').Project3D('xz'), 'Neutron flux <6 meV')
lines = DrawGeometry(lv, zmax)
c20.Print("n20K.pdf")

c300 = ROOT.TCanvas("c300", "c300", 800, 600)
DrawPlot(tallies.Get('tally111_cell0').Project3D('xz'), 'Neutron flux 6-100 meV')
lines = DrawGeometry(lv, zmax)
c300.Print("n300K.pdf")

cfast = ROOT.TCanvas("cfast", "cfast", 800, 600)
cfast.SetLogz()
DrawPlot(tallies.Get('tally121_cell0').Project3D('xz'), 'Neutron flux >100 meV')
lines = DrawGeometry(lv, zmax)
cfast.Print("nfast.pdf")

#ROOT.TGaxis.SetMaxDigits(2)
cspec = ROOT.TCanvas("cspec", "cspec", 800, 600)
cspec.SetLogx()
cspec.SetLogy()
hist = tallies.Get('tally4_cell21').ProjectionX()
hist.Scale(6.2415e12)
hist.GetXaxis().SetTitle('Energy (MeV)')
hist.GetYaxis().SetTitle('Flux (cm^{-2} s^{-1} #muA^{-1})')
hist.SetStats(0)
#hist.GetYaxis().SetRangeUser(1e5, 3e9)
hist.Draw('')
cspec.Print('spectrum.pdf')

ct = ROOT.TCanvas('ctime', 'ctime', 800, 600)
hist = tallies.Get('tally4_cell21')
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
for t,p in zip([76, 86, 96, 106, 116], ['n', '#gamma', 'e', 'p', 'total']):
  hist = ROOT.TH1D(p, p, 13, 7.5, 20.5)
  histd = ROOT.TH1D('delayed '+p, 'delayed '+p, 13, 7.5, 20.5)
  for c in range(1,28):
    tally = tallies.Get('tally{0}_cell{1}'.format(t, c))
    if tally:
      hist.Fill(c, tally.GetBinContent(1))
      for time in range(30, 1170, 240):
        histd.Fill(c, tally.GetBinContent(tally.FindBin(time*1e8)))
  if t == 116:
#    ROOT.gStyle.SetPalette(ROOT.kDarkBodyRadiator)
    heats.Draw('pfc HIST')
    heats.GetYaxis().SetRangeUser(0,2)
    heats.Draw('pfc HIST')
    hist.SetLineColor(ROOT.kRed)
    hist.Draw('SAMEHIST')
  else:
    heats.Add(hist)
    heats.Add(histd)
cheat.BuildLegend(0.5,0.7,0.8,0.85)
cheat.Print('heat.pdf')

cVCN = ROOT.TCanvas('cVCN', 'cVCN', 800, 600)
tally = tallies.Get('tally2_cell71')
eaxis = tally.GetYaxis()
hist = ROOT.TH1D('VCN', 'Guide potential 1 #mueV', eaxis.GetNbins(), eaxis.GetXbins().GetArray())
for eb in range(0, eaxis.GetNbins()):
  energy = eaxis.GetBinCenter(eb)
  if energy < 1e-12 or energy > 1e-9:
    continue
  angle = math.asin(math.sqrt(1e-12/energy))
  cb = tally.GetXaxis().FindBin(math.cos(angle))
  err = ROOT.Double()
  val = tally.IntegralAndError(cb, cb, 0, eb, err)
  hist.SetBinContent(eb, val)
  hist.SetBinError(eb, err)
cVCN.SetLogx()
cVCN.SetLogy()
hist.SetStats(0)
hist.Scale(6.2415e12/1e6, 'width')
hist.GetYaxis().SetTitle("Neutron flux (s^{-1} cm^{-2} #muA^{-1} eV^{-1})")
hist.GetYaxis().SetTitleOffset(1.2)
hist.GetXaxis().SetTitle("Neutron energy (MeV)")
hist.GetXaxis().SetTitleOffset(1.2)
ROOT.gStyle.SetOptTitle(0)
hist.Draw()
cbins = tally.GetXaxis().GetNbins()
maxangle = tally.GetXaxis().GetBinLowEdge(cbins) #get last bin minimum
hist2 = tally.ProjectionY('_py', cbins, cbins)
hist2.SetTitle('Angle <{0:.2g} deg'.format(math.degrees(math.acos(maxangle))))
hist2.Scale(6.2415e12/1e6, 'width')
hist2.SetLineColor(ROOT.kRed)
hist2.Draw('SAME')
cVCN.BuildLegend(0.15,0.7,0.55,0.85)
cVCN.Print('VCN.pdf')
