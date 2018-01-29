import fileinput
import math
import io
import ROOT
import readResults

surfs = readResults.ReadSurfaces(io.FileIO('out1'))
cells = readResults.ReadCells(io.FileIO('out1'))

print 'Simulation for Phase II UCN source.\n'

tallies_file = ROOT.TFile('tallies.root', 'READ')
print 'UCN production in He-II:\n{0[0]:.3g} +- {0[1]:.2g} 1/(s uA)\n'.format(readResults.GetUCNProduction(tallies_file))
      

def print_prompt_heat(tallies_file, cell, name):
  print 'prompt energy deposition in {0} ({1:.3g} l, {2:.3g} kg):\n{3[0]:.3g} +- {3[1]:.2g} mW/uA\n'.format(name, cells[cell]['volume']/1000, cells[cell]['mass']/1000, readResults.GetPromptHeat(tallies_file, cell))

def print_delayed_heat(tallies_file, cell, name):
  print 'delayed energy deposition in {0}:\nmin {1[0]:.3g} +- {1[1]:.2g} mW/uA, max {2[0]:.3g} +- {2[1]:.2g} mW/uA\n'.format(name, readResults.GetMinDelayedHeat(tallies_file, cell), readResults.GetMaxDelayedHeat(tallies_file, cell))

print_prompt_heat(tallies_file, readResults.HeIIcell, 'He-II')
print_prompt_heat(tallies_file, readResults.HeIIbottlecell, 'He-II bottle')
print_delayed_heat(tallies_file, readResults.HeIIcell, 'He-II')
print_delayed_heat(tallies_file, readResults.HeIIbottlecell, 'He-II bottle')
print_prompt_heat(tallies_file, readResults.LD2cell, 'LD2')
print_prompt_heat(tallies_file, readResults.LD2bottlecell, 'LD2 bottle')
print_delayed_heat(tallies_file, readResults.LD2cell, 'LD2')
print_delayed_heat(tallies_file, readResults.LD2bottlecell, 'LD2 bottle')

