import fileinput
import math


### read energy-resolved neutron flux in He-II bottle from ucn_21_tab.lis and sum contribution below 2meV
totalflux = 0.
dflux = 0.
for line in fileinput.input('ucn_21_tab.lis'):
  columns = line.split()
  try:
    Emin = float(columns[0]) # first two columns contain energy bin
    Emax = float(columns[1])
    if Emax > 2e-12:
      break
    print line
    flux = float(columns[2])*(Emax - Emin)*6.2415e12 # multiply differential flux with energy-bin width and scale to beam current of 1uA
    totalflux += flux
    dflux += (float(columns[3])/100.*flux)**2 # add up squared uncertainty of flux
  except ValueError:
    continue
fileinput.close()
dflux = math.sqrt(dflux) # take square root of sum of squared uncertainties

### read *.out files and find lines that contain energy deposition into each region
heII_heat = [] # four components: prompt heat, bottle prompt heat, delayed heat, bottle delayed heat
dheII_heat = [] # corresponding four uncertainties
d2_heat = []
dd2_heat = []
for line in fileinput.input('ucn_22.bnn.asc'):
  if fileinput.filelineno() == 11: # prompt heat
    columns = line.split()
    if len(columns) == 10:
      heII_heat.append(float(columns[3])*1.e9*1.e-6*1000.) # get energy depositions and convert from GeV/proton to mW/uA
      heII_heat.append(float(columns[2])*1.e6)
      d2_heat.append(float(columns[0])*1.e6)
      d2_heat.append((float(columns[1]) + float(columns[8]))*1.e6)
      print line
  elif fileinput.filelineno() == 16 or fileinput.filelineno() == 32: # uncertainties of prompt and delayed heat
    columns = line.split()
    if len(columns) == 10:
      dheII_heat.append(float(columns[3])/100.) # get relative uncertainties
      dheII_heat.append(float(columns[2])/100.)
      dd2_heat.append(float(columns[0])/100.)
      dd2_heat.append(math.sqrt(float(columns[1])**2 + float(columns[8])**2)/100.)
      print line
  elif fileinput.filelineno() == 27: # delayed heat
    columns = line.split()
    if len(columns) == 10:
      heII_heat.append(float(columns[3])*1.e9*1.6021766e-19*1000) # get energy depositions and convert from GeV/s to mW
      heII_heat.append(float(columns[2])*1.e9*1.6021766e-19*1000)
      d2_heat.append(float(columns[0])*1.e9*1.6021766e-19*1000)
      d2_heat.append((float(columns[1]) + float(columns[8]))*1.e9*1.6021766e-19*1000)
      print line
fileinput.close()

print 'cold neutron flux (<2meV) in He-II:\n{0:.3g} +- {1:.2g} 10^12/(cm2 s uA)\n'.format(totalflux/1e12, dflux/1e12)
print 'prompt energy deposition in He-II:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(heII_heat[0], dheII_heat[0]*heII_heat[0])
print 'prompt energy deposition in He-II bottle:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(heII_heat[1], dheII_heat[1]*heII_heat[1])
print 'delayed energy deposition in He-II:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(heII_heat[2], dheII_heat[2]*heII_heat[2])
print 'delayed energy deposition in He-II bottle:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(heII_heat[3], dheII_heat[3]*heII_heat[3])
print 'prompt energy deposition in LD2:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(d2_heat[0], dd2_heat[0]*d2_heat[0])
print 'prompt energy deposition in LD2 bottle:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(d2_heat[1], dd2_heat[1]*d2_heat[1])
print 'delayed energy deposition in LD2:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(d2_heat[2], dd2_heat[2]*d2_heat[2])
print 'delayed energy deposition in LD2 bottle:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(d2_heat[3], dd2_heat[3]*d2_heat[3])

