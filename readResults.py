import re
import math

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'

# read surfaces from stream
def ReadSurfaces(lines):
  surfaces = {}
  for line in lines:
    match = re.match('\s*(\d+)-\s+(\d+)\s+(?:\d*)\s*(RPP|RCC|SO)', line) # find cylinders and boxes
    if match:
      surface = int(match.group(2))
#      print surface
      surfaces[surface] = {}
      surfaces[surface]['shape'] = match.group(3)
      match = re.findall(reg, line)
      surfaces[surface]['size'] = [float(m) for m in match[2:]]
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
    match = re.match('(\s*\d+)-(?:\s*)TMP', line) # find temperature line
    if match:
      match = re.findall('([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?[r]?)\s+', line) # read all temperatures
      cell = 1
      temp = 0.
      for m in match:
        if m.endswith('r'):
	  for i in range(0, int(m[:-1])):
            cells[cell] = {}
            cells[cell]['temp'] = temp
            cell += 1
        else:
          temp = float(m)*11.6045e9
          cells[cell] = {}
          cells[cell]['temp'] = temp
          cell += 1

    match = re.match('\s*(\d+)\s+(\d+)\s+(\d+[s]?)' + reg + reg + reg + reg + '\s+(\d+)' + reg + reg + reg + reg, line) # find volumina and masses
    if match:
      cell = int(match.group(2))
#      print cell
      cells[cell]['volume'] = float(match.group(6))
      cells[cell]['mass'] = float(match.group(7))
  return cells


### read tallies from MCTALMRG
def ReadTallies(lines):
  tal = iter(lines)
  tallies = {}
  line = '\n'
  while line.endswith('\n'):
    line = lines.readline()
    match = re.match('ntal\s+(\d+)', line)
    if match:
      ntally = int(match.group(1))
      line = lines.readline()
      match = re.findall('\s+(\d+)', line)
      for m in match:
        tallies[int(m)] = {}
#      print ntally, tallies
      break

  while line.endswith('\n'):
    tally = 0
    match = re.match('tally\s+(\d+)', line) # find tally
    if not match:
      line = lines.readline()
    else:
      tally = int(match.group(1))
#      print tally
  
      ncells = 0
      while line.endswith('\n'):
        line = lines.readline()
        match = re.match('f'+reg, line) # find number of cells in tally
        if match:
          ncells = int(match.group(1))
          break

      tallies[tally]['cells'] = []
      line = lines.readline()
      match = re.findall('\s+(\d+)', line) # read cells in tally
      for m in match:
        cell = int(m)
        tallies[tally]['cells'].append(cell)
        tallies[tally][cell] = {}
        tallies[tally][cell]['vals'] = []
        tallies[tally][cell]['dvals'] = []
      assert(len(tallies[tally]['cells']) == ncells)
#      print ncells, tallies[tally]['cells']

      ebins = 0
      tbins = 0
      tallies[tally]['ebins'] = []
      tallies[tally]['tbins'] = []
      tallies[tally]['cbins'] = []
      line = lines.readline()
      while not line.startswith('vals'):
        match = re.match('(et|tt|c)\s+(\d+)', line) # find number of bins
        if match and match.group(1) == 'et':
          ebins = int(match.group(2))
          line = lines.readline()
          while line.startswith('  '):
            match = re.findall(reg, line) # read all bins
            for m in match:
              tallies[tally]['ebins'].append(float(m))
            line = lines.readline()
        elif match and match.group(1) == 'tt':
          tbins = int(match.group(2))
          line = lines.readline()
          while line.startswith('  '):
            match = re.findall(reg, line)
            for m in match:
              tallies[tally]['tbins'].append(float(m))
            line = lines.readline()
        elif match and match.group(1) == 'c':
          cbins = int(match.group(2))
          line = lines.readline()
          while line.startswith('  '):
            match = re.findall(reg, line)
            for m in match:
              tallies[tally]['cbins'].append(float(m))
            line = lines.readline()
        else:
          line = lines.readline()

      if cbins == 0:
        tallies[tally]['cbins'].append(1)
        cbins = 1
#      print(cbins, tallies[tally]['cbins'])
      assert(len(tallies[tally]['cbins']) == cbins)
      tallies[tally]['ebins'].append(0)
      if ebins == 0:
        ebins = 1
#      print(ebins, len(tallies[tally]['ebins']))
      assert(len(tallies[tally]['ebins']) == ebins)
      tallies[tally]['tbins'].append(0)
      if tbins == 0:
        tbins = 1
#      print(tbins, len(tallies[tally]['tbins']))
      assert(len(tallies[tally]['tbins']) == tbins)
#      print(tallies[tally])

      i = 0
      line = lines.readline()
      while line.startswith('  '):
        match = re.findall(reg, line) # read all values
        for m in match:
#          print i, nbins, m, tallies[tally]['cells']
          cell = tallies[tally]['cells'][int(i/(ebins*tbins*cbins)/2)]
          if i % 2 == 0:
            tallies[tally][cell]['vals'].append(float(m))
          else:
            tallies[tally][cell]['dvals'].append(float(m)*tallies[tally][cell]['vals'][-1])
          i += 1
        line = lines.readline()
      for c in tallies[tally]['cells']:
        assert(len(tallies[tally][c]['vals']) == ebins*tbins*cbins)
        assert(len(tallies[tally][c]['dvals']) == ebins*tbins*cbins)
  return tallies


def GetUCNProduction(tallies, cells, cell):
  UCNmax = max(tallies[14][cell]['vals'][0] + tallies[14][cell]['dvals'][0], tallies[24][cell]['vals'][0] + tallies[24][cell]['dvals'][0])
  UCNmin = max(tallies[14][cell]['vals'][0] - tallies[14][cell]['dvals'][0], tallies[24][cell]['vals'][0] - tallies[24][cell]['dvals'][0])
  return [(UCNmax + UCNmin)/2*6.2415e12, abs(UCNmax - UCNmin)/2*6.2415e12]

def GetPromptHeat(tallies, cells, cell):
  return [tallies[116][cell]['vals'][0]*cells[cell]['mass'], tallies[116][cell]['dvals'][0]*cells[cell]['mass']]

def GetMaxDelayedHeat(tallies, cells, cell):
  return [sum(tallies[116][cell]['vals'][1:-1:4])*cells[cell]['mass'], 
          math.sqrt(sum(d*d for d in tallies[116][cell]['dvals'][1:-1:4]))*cells[cell]['mass']]

def GetMinDelayedHeat(tallies, cells, cell):
  return [sum(tallies[116][cell]['vals'][4:-1:4])*cells[cell]['mass'], 
          math.sqrt(sum(d*d for d in tallies[116][cell]['dvals'][4:-1:4]))*cells[cell]['mass']]

