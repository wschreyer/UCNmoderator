import fileinput
import math
import numpy
import glob


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
heII_heat = []
heIIbottle_heat = []
for line in fileinput.input(glob.glob('*.out')):
  columns = line.split()
  if len(columns) == 7:
    try:
      if int(columns[0]) == 14 and columns[1] == 'HEII' and columns[2] == '1.000000000D+00':
        heII_heat.append(float(columns[3].replace('D', 'E'))*1.e9*1.6022e-19*6.2415e12*1000.) # get energy deposition into He-II and convert from GeV/proton to mW/uA
        print '{}: {}'.format(fileinput.filename(), line)
      elif int(columns[0]) == 13 and columns[1] == 'HEIIBOTT' and columns[2] == '1.000000000D+00':
        heIIbottle_heat.append(float(columns[3].replace('D', 'E'))*1.e9*1.6022e-19*6.2415e12*1000.) # get energy deposition into He-II bottle and convert from GeV/proton to mW/uA
        print '{}: {}'.format(fileinput.filename(), line)
    except ValueError:
      continue
fileinput.close()

print 'cold neutron (<2meV) flux: {0:.3g} +- {1:.3g} 1/(cm2 s uA)'.format(totalflux, dflux)
print 'heat input into He-II: {0:.2f} +- {1:.2f} mW/uA'.format(numpy.mean(heII_heat), numpy.std(heII_heat))
print 'heat input into He-II bottle: {0:.2f} +- {1:.2f} mW/uA'.format(numpy.mean(heIIbottle_heat), numpy.std(heIIbottle_heat))

