import ROOT
import io
import re
import numpy
import readResults

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


def DrawPlot(gr, xv, yv, vv, title):
  gr.SetTitle(title)
  gr.SetNpx(100)
  gr.SetNpy(70)
  gr.GetHistogram()
  gr.GetXaxis().SetTitle("x (cm)")
  gr.GetXaxis().SetLimits(-100.,100.)
  gr.GetYaxis().SetTitle("z (cm)")
  gr.GetYaxis().SetLimits(-30.,110.)
  gr.Draw("COL1Z")


f = io.open("MESHTALMRG")
xv = []
zv = []
vv = []
for line in f:
  match = re.match(reg+reg+reg+reg+reg, line)
  if match:
    xv.append(float(match.group(1)))
    zv.append(float(match.group(3)))
    vv.append(float(match.group(4))*6.2415e12)
f.close()

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
    if match.group(1) == '21':
      assert(match.group(2) == 'RPP')
      zmax = float(match.group(8))
      break
assert(zmax != -9e99)

c = ROOT.TCanvas("c20", "c20", 800, 600)
c.SetRightMargin(0.12)
gr = ROOT.TGraph2D(7000, numpy.array(xv), numpy.array(zv), numpy.array(vv))
DrawPlot(gr, xv, zv, vv, "Neutron flux <6 meV")
lines = DrawGeometry(lv, zmax)
c.Print("n20K.pdf")

c = ROOT.TCanvas("c300", "c300", 800, 600)
gr = ROOT.TGraph2D(7000, numpy.array(xv[7000:]), numpy.array(zv[7000:]), numpy.array(vv[7000:]))
DrawPlot(gr, xv, zv, vv, "Neutron flux 6-100 meV")
lines = DrawGeometry(lv, zmax)
c.Update()
c.Print("n300K.pdf")

c = ROOT.TCanvas("cfast", "cfast", 800, 600)
c.SetLogz()
gr = ROOT.TGraph2D(7000, numpy.array(xv[14000:]), numpy.array(zv[14000:]), numpy.array(vv[14000:]))
DrawPlot(gr, xv, zv, vv, "Neutron flux >100 meV")
lines = DrawGeometry(lv, zmax)
c.Print("nfast.pdf")

c = ROOT.TCanvas("cspec", "cspec", 800, 600)
c.SetLogx()
c.SetLogy()
tallies = readResults.ReadTallies(io.open('MCTALMRG'))
hist = ROOT.TH1D('spectrum', '', len(tallies[4]['bins']) - 2, numpy.array(tallies[4]['bins'][:-1]))
for i, (val, dval) in enumerate(zip(tallies[4][14]['vals'], tallies[4][14]['dvals'])):
  hist.SetBinContent(i, val*6.2415e12)
  hist.SetBinError(i, dval*6.2415e12)
hist.GetXaxis().SetTitle('Energy (MeV)')
hist.GetYaxis().SetTitle('Flux (cm^{-2} s^{-1} #muA^{-1})')
hist.SetStats(0)
hist.GetYaxis().SetRangeUser(1e5, 3e9)
hist.Draw('')
c.Print("spectrum.pdf")

