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
heII_heat = 0.
heIIbottle_heat = 0.
d2_heat = 0.
d2bottle_heat = 0.
dheII_heat = 0.
dheIIbottle_heat = 0.
dd2_heat = 0.
dd2bottle_beat = 0.
for line in fileinput.input('ucn_22.bnn.asc'):
  if fileinput.filelineno() == 11:
    columns = line.split()
    if len(columns) == 8:
      heII_heat = float(columns[3])*1.e9*1.e-6*1000. # get energy depositions and convert from GeV/proton to mW/uA
      heIIbottle_heat = float(columns[2])*1.e6
      d2_heat = float(columns[0])*1.e6
      d2bottle_heat = float(columns[1])*1.e6
      print line
  elif fileinput.filelineno() == 16:
    columns = line.split()
    if len(columns) == 8:
      dheII_heat = float(columns[3])/100.*heII_heat # get uncertainties and convert from % to mW/uA
      dheIIbottle_heat = float(columns[2])/100.*heIIbottle_heat
      dd2_heat = float(columns[0])/100.*d2_heat
      dd2bottle_heat = float(columns[1])/100.*d2bottle_heat
      print line
fileinput.close()

print 'cold neutron flux (<2meV) in He-II:\n{0:.3g} +- {1:.2g} 10^12/(cm2 s uA)\n'.format(totalflux/1e12, dflux/1e12)
print 'energy deposition in He-II:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(heII_heat, dheII_heat)
print 'energy deposition in He-II bottle:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(heIIbottle_heat, dheIIbottle_heat)
print 'energy deposition in LD2:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(d2_heat, dd2_heat)
print 'energy deposition in LD2 bottle:\n{0:.3g} +- {1:.2g} mW/uA\n'.format(d2bottle_heat, dd2bottle_heat)

