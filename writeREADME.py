import fileinput
import math
import io
import readResults

cells = readResults.ReadCells(io.FileIO('out1'))

print 'Simulation for Phase II UCN source.\n'
print 'Tungsten target with water jacket, encased in lead.'
print 'Cylindrical D2O ({0:.3g} K), LD2 ({1:.3g} K), and He-II ({2:.3g} K) vessels centered above target.'.format(cells[9]['temp'], cells[11]['temp'], cells[14]['temp'])
print 'Sides of D2O vessel covered with graphite reflectors.\n'
print 'Distances above target (cm) + vessel wall thickness:'
target_case = cells[15]['size']
ld2o_bottle = cells[20]['size']
ld2o = cells[19]['size']
print 'Lead - D2O: {0:.3g} + {1:.3g}'.format(ld2o_bottle[2] - target_case[5], ld2o[2] - ld2o_bottle[2])
vac_tank = cells[38]['size']
vac = cells[37]['size']
ld2_bottle = cells[22]['size']
ld2 = cells[23]['size']
print 'D2O - LD2: {0:.3g} + {1:.3g} + {2:.3g} + {3:.3g}'.format(vac_tank[2] - ld2o[2], vac[2] - vac_tank[2], ld2_bottle[2] - vac[2], ld2[2] - ld2_bottle[2])
ld2_ibottle = cells[24]['size']
heii_vac = cells[25]['size']
heii_bottle = cells[35]['size']
heii = cells[36]['size']
print 'LD2 - HE-II: {0:.3g} + {1:.3g} + {2:.3g} + {3:.3g}\n'.format(ld2_ibottle[2] - ld2[2], heii_vac[2] - ld2_ibottle[2], heii_bottle[2] - heii_vac[2], heii[2] - heii_bottle[2])
print 'Outer vessel sizes (cm) - height, radius:'
print 'D2O: {0:.3g}, {1:.3g}'.format(ld2o_bottle[5], ld2o_bottle[6])
print 'LD2: {0:.3g}, {1:.3g}'.format(vac_tank[5], vac_tank[6])
print 'He-II: {0:.3g}, {1:.3g}\n'.format(ld2_ibottle[5], ld2_ibottle[6])


tallies = readResults.ReadTallies(io.FileIO('MCTALMRG'))
print 'UCN production in He-II:\n{0[0]:.3g} +- {0[1]:.2g} 10^4/(s uA)\n'.format(readResults.GetUCNProduction(tallies, cells, 14))
      

def print_prompt_heat(tallies, cells, cell, name):
  print 'prompt energy deposition in {0} ({1:.3g} l, {2:.3g} kg):\n{3[0]:.3g} +- {3[1]:.2g} mW/uA\n'.format(name, cells[cell]['volume']/1000, cells[cell]['mass']/1000, readResults.GetPromptHeat(tallies, cells, cell))

def print_delayed_heat(tallies, cells, cell, name):
  print 'delayed energy deposition in {0}:\nmin {1[0]:.3g} +- {1[1]:.2g} mW/uA, max {2[0]:.3g} +- {2[1]:.2g} mW/uA\n'.format(name, readResults.GetMinDelayedHeat(tallies, cells, cell), readResults.GetMaxDelayedHeat(tallies, cells, cell))

print_prompt_heat(tallies, cells, 14, 'He-II')
print_prompt_heat(tallies, cells, 13, 'He-II bottle')
print_delayed_heat(tallies, cells, 14, 'He-II')
print_delayed_heat(tallies, cells, 13, 'He-II bottle')
print_prompt_heat(tallies, cells, 11, 'LD2')
print_prompt_heat(tallies, cells, 12, 'LD2 bottle')
print_delayed_heat(tallies, cells, 11, 'LD2')
print_delayed_heat(tallies, cells, 12, 'LD2 bottle')


