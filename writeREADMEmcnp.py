import fileinput
import re
import math

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

### read one of the out files and get geometry, masses, volumina, temperatures
volume = {}
mass = {}
temps = []
ld2o_bottle_bottom = 0.0
ld2o_bottle_height = 0.0
ld2o_bottle_radius = 0.0
ld2o_bottom = 0.0
ld2_bottom = 0.0
ld2_bottle_bottom = 0.0
ld2_bottle_height = 0.0
ld2_bottle_radius = 0.0
heii_bottle_bottom = 0.0
heii_bottle_height = 0.0
heii_bottle_radius = 0.0
heii_bottom = 0.0

for line in fileinput.input('out1'):
  match = re.match('\s*(\d+)-\s*(\d+)\s*(RPP|RCC)'+reg+reg+reg+reg+reg+reg+reg+'?', line) # find cylinders and boxes
  if match:
    if int(match.group(2)) == 32: # target casing
      target_top = float(match.group(9))
    elif int(match.group(2)) == 16: # D2O bottle
      ld2o_bottle_bottom = float(match.group(6))
      ld2o_bottle_height = float(match.group(9))
      ld2o_bottle_radius = float(match.group(10))
    elif int(match.group(2)) == 15: # D2O
      ld2o_bottom = float(match.group(6))
    elif int(match.group(2)) == 19: # LD2
      ld2_bottom = float(match.group(6))
    elif int(match.group(2)) == 18: # LD2 bottle
      ld2_bottle_bottom = float(match.group(6))
      ld2_bottle_height = float(match.group(9))
      ld2_bottle_radius = float(match.group(10))
    elif int(match.group(2)) == 20: # He-II bottle
      heii_bottle_bottom = float(match.group(6))
      heii_bottle_height = float(match.group(9))
      heii_bottle_radius = float(match.group(10))
    elif int(match.group(2)) == 21: # He-II
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
print 'D2O - LD2: {0:.3g} + {1:.3g}'.format(ld2_bottle_bottom - ld2o_bottom, ld2_bottom - ld2_bottle_bottom)
print 'LD2 - HE-II: {0:.3g} + {1:.3g}\n'.format(heii_bottle_bottom - ld2_bottom, heii_bottom - heii_bottle_bottom)
print 'Outer vessel sizes (cm) - height, radius:'
print 'D2O: {0:.3g}, {1:.3g}'.format(ld2o_bottle_height, ld2o_bottle_radius)
print 'LD2: {0:.3g}, {1:.3g}'.format(ld2_bottle_height, ld2_bottle_radius)
print 'He-II: {0:.3g}, {1:.3g}\n'.format(heii_bottle_height, heii_bottle_radius)

### read tallies from MCTALMRG, print neutron flux below 2meV and heat deposit in He-II and LD2
state = 'ntal'
tally = 0
ncells = 0
valsfound = False
cells = []
bins = []
vals = []
dvals = []
heats = {}
dheats = {}
for line in fileinput.input('MCTALMRG'):
  if state == 'ntal':
    match = re.match('ntal(\s*\d+)', line)
    if match:
      ntally = int(match.group(1))
      state = 'tally'
      #print 'ntal', ntally
  elif state == 'tally':
    match = re.match('tally(\s*\d+)', line)
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
    match = re.match('(\s*\d+)', line)
    if match:
      for m in re.findall('(\s*\d+)', line):
        cells.append(int(m))
    else:
      #print cells
      state = 'et_vals'
  elif state == 'et_vals':
    if re.match('et(\s*\d+)', line):
      state = 'readbins'
      #print 'et'
    elif line.startswith('vals'):
      state = 'readvals'
      #print 'vals'
  elif state == 'readbins':
    match = re.match(reg, line)
    if match:
      for m in re.findall(reg, line):
        bins.append(float(m))
    else:
      #print bins
      state = 'et_vals'
  elif state == 'readvals':
    match = re.match(reg, line)
    if match:
      for m in re.findall(reg, line)[0::2]:
        vals.append(float(m))
      for m in re.findall(reg, line)[1::2]:
        dvals.append(float(m))
    else:
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
        assert(len(cells) == len(vals) and len(vals) == len(dvals))
        for i, heat, dheat in zip(cells, vals, dvals):
          heats[i] = heat*mass[i]*1000
          dheats[i] = dheat*heats[i]

      state = 'tally'
      #print vals, dvals
      cells = []
      vals = []
      dvals = []
fileinput.close()

print 'prompt energy deposition in He-II ({3:.3g} l, {0:.3g} kg):\n{1:.3g} +- {2:.2g} mW/uA\n'.format(mass[14]/1000, heats[14], dheats[14], volume[14]/1000)
print 'prompt energy deposition in He-II bottle ({3:.3g} l, {0:.3g} kg):\n{1:.3g} +- {2:.2g} mW/uA\n'.format(mass[13]/1000, heats[13], dheats[13], volume[13]/1000)
print 'prompt energy deposition in LD2 ({3:.3g} l, {0:.3g} kg):\n{1:.3g} +- {2:.2g} mW/uA\n'.format(mass[11]/1000, heats[11], dheats[11], volume[11]/1000)
print 'prompt energy deposition in LD2 bottle ({3:.3g} l, {0:.3g} kg):\n{1:.3g} +- {2:.2g} mW/uA\n'.format(mass[12]/1000, heats[12], dheats[12], volume[12]/1000)
#print 'prompt energy deposition in LD2 bottle ({0:.3g} kg):\n{1:.3g} +- {2:.2g} mW/uA\n'.format((mass[12]+mass[19])/1000, heats[12]+heats[19], dheats[12]+dheats[19])

