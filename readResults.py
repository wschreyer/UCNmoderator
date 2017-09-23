import re
import math

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'


### read cells from stream
def ReadCells(lines):
  cells = {}
  for line in lines:
    match = re.match('\s*(\d+)-\s*(\d+)\s*(RPP|RCC|SO)', line) # find cylinders and boxes
    if match:
      cell = int(match.group(2))
#      print cell
      cells[cell] = {}
      cells[cell]['shape'] = match.group(3)
      match = re.findall(reg, line)
      cells[cell]['size'] = [float(m) for m in match[2:]]

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
        match = re.match('f\s+(\d+)', line) # find number of cells in tally
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

      nbins = 0
      tallies[tally]['bins'] = []
      line = lines.readline()
      while not line.startswith('vals'):
        match = re.match('(et|tt)\s+(\d+)', line) # find number of bins
        line = lines.readline()
        if match:
          nbins = int(match.group(2))
          break

      while nbins > 0 and line.startswith('  '):
        match = re.findall(reg, line) # read all bins
        for m in match:
          tallies[tally]['bins'].append(float(m))
        line = lines.readline()
      tallies[tally]['bins'].append(0)
      if nbins == 0:
        nbins = 1
#      print nbins, tallies[tally]['bins']
      assert(len(tallies[tally]['bins']) == nbins)

      while not line.startswith('vals'):
        line = lines.readline()

      i = 0
      line = lines.readline()
      while line.startswith('  '):
        match = re.findall(reg, line) # read all values
        for m in match:
#          print i, nbins, m, tallies[tally]['cells']
          cell = tallies[tally]['cells'][math.floor(i/nbins/2)]
          if i % 2 == 0:
            tallies[tally][cell]['vals'].append(float(m))
          else:
            tallies[tally][cell]['dvals'].append(float(m)*tallies[tally][cell]['vals'][-1])
          i += 1
        line = lines.readline()
      for c in tallies[tally]['cells']:
        assert(len(tallies[tally][c]['vals']) == nbins)
        assert(len(tallies[tally][c]['dvals']) == nbins)
#        print c, tallies[tally][c]
  return tallies


def GetUCNProduction(tallies, cells, cell):
  UCNmax = max(tallies[14][cell]['vals'][0] + tallies[14][cell]['dvals'][0], tallies[24][cell]['vals'][0] + tallies[24][cell]['dvals'][0])
  UCNmin = max(tallies[14][cell]['vals'][0] - tallies[14][cell]['dvals'][0], tallies[24][cell]['vals'][0] - tallies[24][cell]['dvals'][0])
  return [(UCNmax + UCNmin)/2*6.2415e12/1e4, abs(UCNmax - UCNmin)/2*6.2415e12/1e4]

def GetPromptHeat(tallies, cells, cell):
  return [tallies[116][cell]['vals'][0]*cells[cell]['mass']*1000, tallies[116][cell]['dvals'][0]*cells[cell]['mass']*1000]

def GetMaxDelayedHeat(tallies, cells, cell):
  return [sum(tallies[116][cell]['vals'][1:-1:4])*cells[cell]['mass']*1000, 
          math.sqrt(sum(d*d for d in tallies[116][cell]['dvals'][1:-1:4]))*cells[cell]['mass']*1000]

def GetMinDelayedHeat(tallies, cells, cell):
  return [sum(tallies[116][cell]['vals'][4:-1:4])*cells[cell]['mass']*1000, 
          math.sqrt(sum(d*d for d in tallies[116][cell]['dvals'][4:-1:4]))*cells[cell]['mass']*1000]

