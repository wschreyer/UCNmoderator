import re
import math
import ROOT

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'

# read surfaces from stream
def ReadSurfaces(lines):
  surfaces = {}
  for line in lines:
    match = re.match('\s*(\d+)-\s+(\d+)\s+(\d+)?\s+(RPP|RCC|SO)', line) # find cylinders and boxes
    if match:
      surface = int(match.group(2))
      trafo = 0
      if match.group(3):
        trafo = 1
#      print surface
      surfaces[surface] = {}
      surfaces[surface]['shape'] = match.group(3 + trafo)
      match = re.findall(reg, line)
      surfaces[surface]['size'] = [float(m) for m in match[2 + trafo:]]
      size = surfaces[surface]['size']
      if surfaces[surface]['shape'] == 'RPP':
        surfaces[surface]['area'] = 2*(size[1] - size[0])*(size[3] - size[2] + size[5] - size[4]) + 2*(size[5] - size[4])*(size[3] - size[2])
      elif surfaces[surface]['shape'] == 'RCC':
        surfaces[surface]['area'] = 2*size[6]**2*math.pi + 2*size[6]*math.pi*math.sqrt(size[3]**2 + size[4]**2 + size[5]**2)
      elif surfaces[surface]['shape'] == 'S0':
        surfaces[surface]['area'] = 4.*size[0]**2*math.pi
  return surfaces

### read cells from stream
def ReadCells(lines):
  cells = {}
  for line in lines:
    match = re.match('\s*(\d+)-\s+(\d+)\s+(\d+)' + reg, line) #find cell lines
    if match:
      cell = int(match.group(2))
      cells[cell] = {}
      if match.group(3) != 0:
        cells[cell]['density'] = float(match.group(4))
      else:
        cells[cell]['density'] = 0

    match = re.match('(\s*\d+)-(?:\s*)TMP', line) # find temperature line
    if match:
      match = re.findall('([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?[r]?)\s+', line) # read all temperatures
      cell = 1
      temp = 0.
      for m in match:
        if m.endswith('r'):
	  for i in range(0, int(m[:-1])):
            cells[cell]['temp'] = temp
            cell += 1
        else:
          temp = float(m)*11.6045e9
          cells[cell]['temp'] = temp
          cell += 1

    match = re.match('\s*(\d+)\s+(\d+)\s+(\d+[s]?)' + reg + reg + reg + reg + '\s+(\d+)' + reg + reg + reg + reg, line) # find volumina and masses
    if match:
      cell = int(match.group(2))
#      print cell
      cells[cell]['volume'] = float(match.group(6))
      cells[cell]['mass'] = float(match.group(7))
  return cells

### read materials from stream
def ReadMaterials(lines):
  materials = {}
  for line in lines:  
    match = re.match('(\s*\d+)-\s+M(\d+)', line) #find material entries
    if match:
      material = int(match.group(2))
      match = re.findall('\s+(\d+)'+reg, line)
      materials[material] = []
      for m in match:
        materials[material].append([int(m[0]), float(m[1])])
  return materials

HeIIcell = 16
HeIIbottlecell = 17
sD2Ocell = 21
sD2Obottlecell = 27
D2Ocell = 22
D2Obottlecell = 20
hexchcell = 29
He3cell = 30
guidecell = 31

def GetUCNProduction(tallies_file):
  tally14 = tallies_file.Get('tally14')
  tally24 = tallies_file.Get('tally24')
  b14 = tally14.FindBin(HeIIcell)
  b24 = tally24.FindBin(HeIIcell)
  prod14 = [tally14.GetBinContent(b14), tally14.GetBinError(b14)]
  prod24 = [tally24.GetBinContent(b24), tally24.GetBinError(b24)]
  UCNmax = max(prod14[0] + prod14[1], prod24[0] + prod24[1])
  UCNmin = max(prod14[0] - prod14[1], prod24[0] - prod24[1])
  return [(UCNmax + UCNmin)/2*6.2415e12, abs(UCNmax - UCNmin)/2*6.2415e12]

def GetPromptHeat(tallies_file, cell, tally = 116):
  tally = tallies_file.Get('tally{1}_cell{0}'.format(cell, tally))
  return [tally.GetBinContent(1)*1000, tally.GetBinError(1)*1000]

def GetMaxDelayedHeat(tallies_file, cell, tally = 116):
  tally = tallies_file.Get('tally{1}_cell{0}'.format(cell, tally))
  heat = [0,0]
  for t in range(30, 1200, 240):
    b = tally.FindBin(t*1e8)
    heat = [heat[0] + tally.GetBinContent(b), heat[1] + tally.GetBinError(b)**2]
  b = tally.FindBin(1800e8)
  heat = [heat[0] + tally.GetBinContent(b)/4, heat[1] + tally.GetBinError(b)**2/16]
  return [heat[0]*1000, math.sqrt(heat[1])*1000]


def GetMinDelayedHeat(tallies_file, cell, tally = 116):
  tally = tallies_file.Get('tally{1}_cell{0}'.format(cell, tally))
  heat = [0,0]
  for t in range(210, 1200, 240):
    b = tally.FindBin(t*1e8)
    heat = [heat[0] + tally.GetBinContent(b), heat[1] + tally.GetBinError(b)**2]
  b = tally.FindBin(1800e8)
  heat = [heat[0] + tally.GetBinContent(b)/4, heat[1] + tally.GetBinError(b)**2/16]
  return [heat[0]*1000, math.sqrt(heat[1])*1000]

def GetTritiumProduction(tallies_file, cell):
  t = 0
  if cell == D2Ocell:
    t = 134
  elif cell == sD2Ocell:
    t = 144
  elif cell == He3cell:
    t = 154
  else:
    assert(True)
  tally = tallies_file.Get('tally{0}'.format(t, cell))
  b = tally.FindBin(cell)
  factor = 6.241509e12*86400*1.782786e-9 #production rate per day times activity
  return [tally.GetBinContent(b)*factor, tally.GetBinError(b)*factor]
