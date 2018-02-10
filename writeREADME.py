import fileinput
import math
import io
import ROOT
import readResults

surfs = readResults.ReadSurfaces(io.FileIO('out1'))
cells = readResults.ReadCells(io.FileIO('out1'))

print 'Simulation for Phase II UCN source.\n'

tallies_file = ROOT.TFile('tallies.root', 'READ')

prod = readResults.GetUCNProduction(tallies_file)
heat = [0.,0.]
for cell in [readResults.HeIIcell, readResults.HeIIbottlecell]:
  h = readResults.GetPromptHeat(tallies_file, cell)
  heat[0] = heat[0] + h[0]
  heat[1] = math.sqrt(heat[1]**2 + h[1]**2)
  h = readResults.GetMaxDelayedHeat(tallies_file, cell)
  heat[0] = heat[0] + h[0]
  heat[1] = math.sqrt(heat[1]**2 + h[1]**2)
pph = [prod[0]/heat[0], math.sqrt((prod[1]/prod[0])**2 + (heat[1]/heat[0])**2)*prod[0]/heat[0]]
print('Production-to-heat ratio:\n{0[0]:.3g} +- {0[1]:.2g} 1/(s mW)\n'.format(pph))

print 'UCN production in He-II:\n{0[0]:.3g} +- {0[1]:.2g} 1/(s uA)\n'.format(prod)

print('Total heat in He-II:\n{0[0]:.3g} +- {0[1]:.2g} mW/uA\n'.format(heat))      

def print_prompt_heat(tallies_file, cell, name):
  print 'prompt energy deposition in {0} ({1:.3g} l, {2:.3g} kg):\n{3[0]:.3g} +- {3[1]:.2g} mW/uA\n'.format(name, cells[cell]['volume']/1000, cells[cell]['mass']/1000, readResults.GetPromptHeat(tallies_file, cell))

def print_delayed_heat(tallies_file, cell, name):
  print 'delayed energy deposition in {0}:\nmin {1[0]:.3g} +- {1[1]:.2g} mW/uA, max {2[0]:.3g} +- {2[1]:.2g} mW/uA\n'.format(name, readResults.GetMinDelayedHeat(tallies_file, cell), readResults.GetMaxDelayedHeat(tallies_file, cell))

def print_tritium_production(tallies_file, cell, name):
  print 'Tritium production in {0}:\n{1[0]:.3g} +- {1[1]:.2g} Bq/d/uA\n'.format(name, readResults.GetTritiumProduction(tallies_file, cell))

print_prompt_heat(tallies_file, readResults.HeIIcell, 'He-II')
print_prompt_heat(tallies_file, readResults.HeIIbottlecell, 'He-II bottle')
print_prompt_heat(tallies_file, readResults.guidecell, 'UCN guide')
print_delayed_heat(tallies_file, readResults.HeIIcell, 'He-II')
print_delayed_heat(tallies_file, readResults.HeIIbottlecell, 'He-II bottle')
print_delayed_heat(tallies_file, readResults.guidecell, 'UCN guide')
print_prompt_heat(tallies_file, readResults.sD2Ocell, 'sD2O')
print_prompt_heat(tallies_file, readResults.sD2Obottlecell, 'sD2O bottle')
print_delayed_heat(tallies_file, readResults.sD2Ocell, 'sD2O')
print_delayed_heat(tallies_file, readResults.sD2Obottlecell, 'sD2O bottle')
print_prompt_heat(tallies_file, readResults.hexchcell, 'Heat exchanger')
print_prompt_heat(tallies_file, readResults.He3cell, '3He')
print_delayed_heat(tallies_file, readResults.hexchcell, 'Heat exchanger')
print_delayed_heat(tallies_file, readResults.He3cell, '3He')
print_prompt_heat(tallies_file, readResults.D2Ocell, 'D2O')
print_prompt_heat(tallies_file, readResults.D2Obottlecell, 'D2O bottle')
print_delayed_heat(tallies_file, readResults.D2Ocell, 'D2O')
print_delayed_heat(tallies_file, readResults.D2Obottlecell, 'D2O bottle')
print_tritium_production(tallies_file, readResults.D2Ocell, 'D2O')
print_tritium_production(tallies_file, readResults.sD2Ocell, 'sD2O')
print_tritium_production(tallies_file, readResults.He3cell, '3He')
