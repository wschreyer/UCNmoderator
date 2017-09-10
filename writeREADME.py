import fileinput
import re
import math
import collections
import numpy

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

### read one of the out files and get geometry, masses, volumina, temperatures
volume = {}
mass = {}
temps = []
target_top = 0.0
ld2o_bottle_bottom = 0.0
ld2o_bottle_height = 0.0
ld2o_bottle_radius = 0.0
ld2o_bottom = 0.0
vac_tank_bottom = 0.0
vac_tank_height = 0.0
vac_tank_radius = 0.0
vac_bottom = 0.0
ld2_bottle_bottom = 0.0
ld2_bottom = 0.0
ld2_ibottle_bottom = 0.0
ld2_ibottle_height = 0.0
ld2_ibottle_radius = 0.0
heii_vac_bottom = 0.0
heii_bottle_bottom = 0.0
heii_bottom = 0.0

for line in fileinput.input('out1'):
  match = re.match('\s*(\d+)-\s*(\d+)\s*(RPP|RCC)'+reg+reg+reg+reg+reg+reg+reg+'?', line) # find cylinders and boxes
  if match:
    if int(match.group(2)) == 15: # target casing
      target_top = float(match.group(9))
    elif int(match.group(2)) == 20: # D2O bottle
      ld2o_bottle_bottom = float(match.group(6))
      ld2o_bottle_height = float(match.group(9))
      ld2o_bottle_radius = float(match.group(10))
    elif int(match.group(2)) == 19: # D2O
      ld2o_bottom = float(match.group(6))
    elif int(match.group(2)) == 38: # cryostat tank
      vac_tank_bottom = float(match.group(6))
      vac_tank_height = float(match.group(9))
      vac_tank_radius = float(match.group(10))
    elif int(match.group(2)) == 37: # insulating vacuum
      vac_bottom = float(match.group(6))
    elif int(match.group(2)) == 22: # LD2 bottle
      ld2_bottle_bottom = float(match.group(6))
    elif int(match.group(2)) == 23: # LD2
      ld2_bottom = float(match.group(6))
    elif int(match.group(2)) == 24: # inner LD2 bottle
      ld2_ibottle_bottom = float(match.group(6))
      ld2_ibottle_height = float(match.group(9))
      ld2_ibottle_radius = float(match.group(10))
    elif int(match.group(2)) == 25: # He-II insulating vacuum
      heii_vac_bottom = float(match.group(6))
    elif int(match.group(2)) == 35: # He-II bottle
      heii_bottle_bottom = float(match.group(6))
    elif int(match.group(2)) == 36: # He-II
      heii_bottom = float(match.group(6))

  match = re.match('(\s*\d+)-(?:\s*)TMP', line) # find temperature line
  if match:
    match = re.findall('\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?r?)', line) # read all temperatures
    for m in match:
      if m.endswith('r'):
        for i in range(0, int(m[:-1])):
          temps.append(temp)
      else:
        temp = float(m)*11.6045e9
        temps.append(temp)

  match = re.match('\s*(\d+)\s*(\d+)\s*(\d+[s]?)' + reg + reg + reg + reg + '\s*(\d+)' + reg + reg + reg + reg, line) # find volumina and masses
  if match:
    cell = int(match.group(2))
    volume[cell] = float(match.group(6))
    mass[cell] = float(match.group(7))
fileinput.close()

#print volume
#print mass
#print temps

print 'Simulation for Phase II UCN source.\n'
print 'Tungsten target with water jacket, encased in lead.'
print 'Cylindrical D2O ({0:.3g} K), LD2 ({1:.3g} K), and He-II ({2:.3g} K) vessels centered above target.'.format(temps[9], temps[11], temps[14])
print 'Sides of D2O vessel covered with graphite reflectors.\n'
print 'Distances above target (cm) + vessel wall thickness:'
print 'Target - D2O: {0:.3g} + {1:.3g}'.format(ld2o_bottle_bottom, ld2o_bottom - ld2o_bottle_bottom)
print 'D2O - LD2: {0:.3g} + {1:.3g} + {2:.3g} + {3:.3g}'.format(vac_tank_bottom - ld2o_bottom, vac_bottom - vac_tank_bottom, ld2_bottle_bottom - vac_bottom, ld2_bottom - ld2_bottle_bottom)
print 'LD2 - HE-II: {0:.3g} + {1:.3g} + {2:.3g} + {3:.3g}\n'.format(ld2_ibottle_bottom - ld2_bottom, heii_vac_bottom - ld2_ibottle_bottom, heii_bottle_bottom - heii_vac_bottom, heii_bottom - heii_bottle_bottom)
print 'Outer vessel sizes (cm) - height, radius:'
print 'D2O: {0:.3g}, {1:.3g}'.format(ld2o_bottle_height, ld2o_bottle_radius)
print 'LD2: {0:.3g}, {1:.3g}'.format(vac_tank_height, vac_tank_radius)
print 'He-II: {0:.3g}, {1:.3g}\n'.format(ld2_ibottle_height, ld2_ibottle_radius)

### read tallies from MCTALMRG, print neutron flux below 2meV and heat deposit in He-II and LD2
state = 'ntal'
tally = 0
valsfound = False
ncells = 0
cells = []
nbins = 1
bins = []
vals = []
dvals = []
heats = collections.defaultdict(list)
dheats = collections.defaultdict(list)
for line in fileinput.input('MCTALMRG'):
  if state == 'ntal':
    match = re.match('ntal\s*(\d+)', line)
    if match:
      ntally = int(match.group(1))
      state = 'tally'
      #print 'ntal', ntally
  elif state == 'tally':
    match = re.match('tally\s*(\d+)', line)
    if match:
      tally = int(match.group(1))
      #print 'tally: {0}'.format(tally)
      state = 'f'
  elif state == 'f':
    match = re.match('f\s*(\d+)', line)
    if match:
      ncells = int(match.group(1))
      #print 'ncells: {0}'.format(ncells)
      state = 'cells'
  elif state == 'cells':
    match = re.match('\s*(\d+)', line)
    if match:
      for m in re.findall('(\s*\d+)', line):
        cells.append(int(m))
    if len(cells) == ncells:
      #print cells
      state = 'bins_or_vals'
  elif state == 'bins_or_vals':
    match = re.match('[et]t\s*(\d+)', line)
    if match:
      nbins = int(match.group(1))
      #print 'bins:', nbins
      state = 'readbins'
    elif line.startswith('vals'):
      state = 'readvals'
      #print 'vals'
  elif state == 'readbins':
    match = re.match(reg, line)
    if match:
      for m in re.findall(reg, line):
        bins.append(float(m))
    if len(bins) == nbins - 1:
      #print bins
      state = 'bins_or_vals'
  elif state == 'readvals':
    match = re.match(reg, line)
    if match:
      for m in re.findall(reg, line)[0::2]:
        vals.append(float(m))
      for m in re.findall(reg, line)[1::2]:
        dvals.append(float(m))
    if len(vals) == ncells*nbins:

      if tally == 4:
        totalflux = 0
        dtotalflux = 0
        assert(len(bins) == len(vals) - 1 and len(vals) == len(dvals))
        for Energy, Flux, dFlux in zip(bins, vals, dvals):
          if Energy <= 2e-9:
            totalflux += Flux
            dtotalflux += dFlux*dFlux*Flux*Flux
        totalflux *= volume[14]*6.2415e12
        dtotalflux = volume[14]*6.2415e12*math.sqrt(dtotalflux)
        print 'cold neutron flux (<2meV) in He-II:\n{0:.3g} +- {1:.2g} 10^12/(cm2 s uA)\n'.format(totalflux/1e12, dtotalflux/1e12)
      
      if tally == 116:
        i = 0
        for cell in cells:
          for bin in bins:
            heats[cell].append(vals[i]*mass[cell]*1000.)
            dheats[cell].append(dvals[i]*vals[i]*mass[cell]*1000)
            i += 1
          i += 1 # skip total heat deposit

      state = 'tally'
      #print vals, dvals
      cells = []
      nbins = 1
      bins = []
      vals = []
      dvals = []
fileinput.close()

#print heats, dheats

def print_prompt_heat(cell, name):
  print 'prompt energy deposition in {0} ({1:.3g} l, {2:.3g} kg):\n{3:.3g} +- {4:.2g} mW/uA\n'.format(name, volume[cell]/1000, mass[cell]/1000, heats[cell][0], dheats[cell][0])
def print_delayed_heat(cell, name):
  maxheat = sum(heats[cell][1::4]) # max heat right after fifth irradiation (after 17 min) is given by convolution of irradiation profile with decay function, results in sum of integrals of decay heat over irradiation times (1 min on, 3 min off)
  dmaxheat = math.sqrt(sum(d*d for d in dheats[cell][1::4]))
  minheat = sum(heats[cell][4::4]) # min heat right before sixth irradiation (after 20min)
  dminheat = math.sqrt(sum(d*d for d in dheats[cell][4::4]))
  print 'delayed energy deposition in {0}:\nmin {1:.3g} +- {2:.2g} mW/uA, max {3:.3g} +- {4:.2g} mW/uA\n'.format(name, minheat, dminheat, maxheat, dmaxheat)

print_prompt_heat(14, 'He-II')
print_prompt_heat(13, 'He-II bottle')
print_delayed_heat(14, 'He-II')
print_delayed_heat(13, 'He-II bottle')
print_prompt_heat(11, 'LD2')
print_prompt_heat(12, 'LD2 bottle')
print_delayed_heat(11, 'LD2')
print_delayed_heat(12, 'LD2 bottle')


