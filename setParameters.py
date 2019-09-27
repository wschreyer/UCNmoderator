from __future__ import print_function

import fileinput
import re
import math
import scipy.optimize

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'

ld2length = 7.0
helength = 3.6

def SetSize(name, number, type, sizeindices, newsizes, inpfile, mcnpfile):
  for line in fileinput.input(inpfile, inplace = 1):
    match = re.match('\s*(\w+)\s+(\w+)'+reg, line)
    if match:
      m = list(match.groups())
      if m[1] == name:
        assert(m[0] == type)
        print(m[0] + ' ' + m[1], end = ' ')
        m = re.findall(reg, line)
        for i,size in zip(sizeindices, newsizes):
          m[i] = '{0:g}'.format(size)
        for i in m:
          print(i, end = ' ')
        print('')
      else:
        print(line, end = '')
    else:
      print(line, end = '')
  fileinput.close()

  if type == 'SPH':
    type = 'S'
  elif type == 'XZP':
    type = 'PY'
  for line in fileinput.input(mcnpfile, inplace = 1):
    match = re.match('\s*(\d+)\s+(\w+)'+reg, line)
    if match:
      m = list(match.groups())
      if int(m[0]) == number:
        assert(m[1] == type)
        print(m[0] + ' ' + m[1], end = ' ')
        m = re.findall(reg, line)
        for i,size in zip(sizeindices, newsizes):
          m[i] = '{0:g}'.format(size)
        for i in m:
          print(i, end = ' ')
        print('')
      else:
        print(line, end = '')
    else:
      print(line, end = '')
  fileinput.close()

def SetTranslation(name, number, x, y, z, inpfile, mcnpfile):
  for line in fileinput.input(inpfile, inplace = 1):
    if line.startswith('ROT-DEFI                                ') and line.endswith(name+'\n'):
      print('ROT-DEFI  {0:40g}{1:10g}{2:10g}{3}'.format(x,y,z,name))
    else:
      print(line, end = '')

  for line in fileinput.input(mcnpfile, inplace = 1):
    match = re.match('\s*TR(\d+)'+reg+reg+reg+'(.*)', line)
    if match and int(match.group(1)) == number:
      print('TR' + match.group(1) + ' ' + '{0:g} {1:g} {2:g}'.format(x, y, z) + match.group(5))
    else:
      print(line, end = '')
      

def SetParameters(xoff, yoff, inpfile, mcnpfile):
  SetTranslation('BeamRot', 1, xoff, yoff, 0, inpfile, mcnpfile)
  SetTranslation('TgtOffset', 4, xoff, yoff, 0, inpfile, mcnpfile)

bounds = ((-50., 50.), (-50., 50.))
