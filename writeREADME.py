import fileinput
import math
import io
import ROOT
import readResults

surfs = readResults.ReadSurfaces(io.FileIO('out1'))
cells = readResults.ReadCells(io.FileIO('out1'))

print 'Simulation for Phase II UCN source.\n'
print 'Tungsten target with water jacket, encased in lead.'
target_offset = surfs[3]['size'][0] + 0.4
print 'Cylindrical D2O ({0:.3g} K), LD2 ({1:.3g} K), and He-II ({2:.3g} K) vessels offset {3:.3g} cm from target.'.format(cells[9]['temp'], cells[11]['temp'], cells[14]['temp'], target_offset)
print 'Sides of D2O vessel covered with graphite reflectors.\n'
print 'Distances above target (cm) + vessel wall thickness:'
target_case = surfs[15]['size']
ld2o_bottle = surfs[20]['size']
ld2o = surfs[19]['size']
print 'Lead - D2O: {0:.3g} + {1:.3g}'.format(ld2o_bottle[2] - target_case[5], ld2o[2] - ld2o_bottle[2])
vac_tank = surfs[38]['size']
vac = surfs[37]['size']
ld2_bottle = surfs[22]['size']
ld2 = surfs[23]['size']
print 'D2O - LD2: {0:.3g} + {1:.3g} + {2:.3g} + {3:.3g}'.format(vac_tank[2] - ld2o[2], vac[2] - vac_tank[2], ld2_bottle[2] - vac[2], ld2[2] - ld2_bottle[2])
ld2_ibottle = surfs[24]['size']
heii_vac = surfs[25]['size']
heii_bottle = surfs[35]['size']
heii = surfs[36]['size']
print 'LD2 - HE-II: {0:.3g} + {1:.3g} + {2:.3g} + {3:.3g}\n'.format(ld2_ibottle[2] - ld2[2], heii_vac[2] - ld2_ibottle[2], heii_bottle[2] - heii_vac[2], heii[2] - heii_bottle[2])
print 'Outer vessel sizes (cm) - height, radius:'
print 'D2O: {0:.3g} {1:.3g}'.format(ld2o_bottle[5], ld2o_bottle[6])
print 'LD2: {0:.3g} {1:.3g}'.format(vac_tank[5], vac_tank[6])
print 'He-II: {0:.3g} {1:.3g}\n'.format(ld2_ibottle[5], ld2_ibottle[6])

tallies_file = ROOT.TFile('tallies.root', 'READ')
print 'UCN production in He-II:\n{0[0]:.3g} +- {0[1]:.2g} 1/(s uA)\n'.format(readResults.GetUCNProduction(tallies_file, 14))
      

def print_prompt_heat(tallies_file, cell, name):
  print 'prompt energy deposition in {0} ({1:.3g} l, {2:.3g} kg):\n{3[0]:.3g} +- {3[1]:.2g} mW/uA\n'.format(name, cells[cell]['volume']/1000, cells[cell]['mass']/1000, readResults.GetPromptHeat(tallies_file, cell))

def print_delayed_heat(tallies_file, cell, name):
  print 'delayed energy deposition in {0}:\nmin {1[0]:.3g} +- {1[1]:.2g} mW/uA, max {2[0]:.3g} +- {2[1]:.2g} mW/uA\n'.format(name, readResults.GetMinDelayedHeat(tallies_file, cell), readResults.GetMaxDelayedHeat(tallies_file, cell))

print_prompt_heat(tallies_file, 14, 'He-II')
print_prompt_heat(tallies_file, 13, 'He-II bottle')
print_delayed_heat(tallies_file, 14, 'He-II')
print_delayed_heat(tallies_file, 13, 'He-II bottle')
print_prompt_heat(tallies_file, 11, 'LD2')
print_prompt_heat(tallies_file, 12, 'LD2 bottle')
print_delayed_heat(tallies_file, 11, 'LD2')
print_delayed_heat(tallies_file, 12, 'LD2 bottle')


