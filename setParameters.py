from __future__ import print_function

import fileinput
import re
import math
import random

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'

def SetSize(name, number, type, sizeindices, newsizes, inpfile = 'ucn.inp', mcnpfile = 'ucn.mcnp'):
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

def SetTranslation(name, number, x, y, z, inpfile = 'ucn.inp', mcnpfile = 'ucn.mcnp'):
  for line in fileinput.input(inpfile, inplace = 1):
    if line.startswith('ROT-DEFI') and line.endswith(name+'\n'):
      print('ROT-DEFI  {0:40g}{1:10g}{2:10g}{3}'.format(x,y,z,name))
    else:
      print(line, end = '')

  for line in fileinput.input(mcnpfile, inplace = 1):
    match = re.match('\s*TR(\d+)'+reg+reg+reg, line)
    if match and int(match.group(1)) == number:
      print('TR' + match.group(1) + ' ' + '{0:g} {1:g} {2:g}'.format(x, y, z))
    else:
      print(line, end = '')
      

def LD2volume(ld2pos, ld2radius, ld2length, hepos, heradius):
  outervol = 2./3.*ld2radius**3*math.pi + ld2radius**2*math.pi*ld2length
  innerradius = heradius + 3.16
  innerlength = ld2length - (ld2pos - hepos)
  innervol = 2./3.*innerradius**3*math.pi + innerradius**2*math.pi*innerlength
  return outervol - innervol

def SetParameters(lead, d2othickness, ld2pos, ld2radius, ld2length, hepos, heradius, helength, heoffset):
  tgttop = 13.7
  d2oy = ld2pos - ld2length - 11
  d2oz = tgttop + lead + d2othickness + 2*ld2radius + 2*8.46 + 10
  SetSize('ld2o',     51, 'RPP', [2,3,4,5], [d2oy, ld2pos + ld2radius + 21.56, tgttop + lead + 0.3, d2oz - 0.3])
  SetSize('ld2obott', 52, 'RPP', [2,3,4,5], [d2oy - 0.3, ld2pos + ld2radius + 21.86, tgttop + lead, d2oz])
  SetSize('reflecto', 53, 'RPP', [4,5], [tgttop + lead, d2oz + 30])
  SetSize('srcpit',   54, 'RPP', [4,5], [tgttop + lead, d2oz + 30])
  ld2z = tgttop + lead + d2othickness + ld2radius + 8.46
  SetSize('ld2bottl', 55, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - 1, ld2radius + 0.36])
  SetSize('ld2',      56, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length, ld2radius])
  heheight = ld2z + heoffset
  SetSize('ld2i',     57, 'RCC', [1,2,4,6], [hepos, heheight, -ld2length + (ld2pos - hepos) - 0.1, heradius + 3.16])
  SetSize('ld2ibott', 58, 'RCC', [1,2,4,6], [hepos, heheight, -ld2length + (ld2pos - hepos) - 1.1, heradius + 2.8])
  SetSize('heiibott', 59, 'RCC', [1,2,4,6], [hepos, heheight, -helength, heradius + 0.3])
  SetSize('heii',     60, 'RCC', [1,2,4,6], [hepos, heheight, -helength, heradius])
  SetSize('d2oibott', 61, 'RCC', [1,2,4,6], [ld2pos, ld2z, d2oy - 0.3 - ld2pos - 0.1, ld2radius + 7.86])
  SetSize('ld2oi',    62, 'RCC', [1,2,4,6], [ld2pos, ld2z, d2oy - ld2pos - 0.1, ld2radius + 8.16])
  SetSize('heiilow' , 63, 'SPH', [1,2,3], [hepos, heheight, heradius])
  SetSize('heiiup',   64, 'SPH', [1,2,3], [hepos - helength, heheight, heradius])
  SetSize('hebottup', 65, 'SPH', [1,2,3], [hepos - helength, heheight, heradius + 0.3])
  SetSize('hebottlo', 66, 'SPH', [1,2,3], [hepos, heheight, heradius + 0.3])
  SetSize('ld2ibolo', 67, 'SPH', [1,2,3], [hepos, heheight, heradius + 2.8])
  SetSize('ld2ilow',  68, 'SPH', [1,2,3], [hepos, heheight, heradius + 3.16])
  SetSize('ld2low',   69, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius])
  SetSize('ld2botlo', 70, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 0.36])
  SetSize('thshldli', 71, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 2.26])
  SetSize('thshldlo', 72, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 2.41])
  SetSize('vactnkli', 73, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 6.2])
  SetSize('vactnklo', 74, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 6.56])
  SetSize('d2oibolo', 75, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 7.86])
  SetSize('d2oilow',  76, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 8.16])
  SetSize('vacsepli', 77, 'SPH', [1,2,3], [hepos, heheight, heradius + 1.55])
  SetSize('vacseplo', 78, 'SPH', [1,2,3], [hepos, heheight, heradius + 1.7])
  SetSize('ld2pos',   79, 'XZP', [0], [ld2pos])
  SetSize('hepos',    80, 'XZP', [0], [hepos])
  SetSize('vacsepi',  81, 'RCC', [1,2,4,6], [hepos, heheight, -helength - heradius, heradius + 1.55])
  SetSize('vacsepo',  82, 'RCC', [1,2,4,6], [hepos, heheight, -helength - heradius, heradius + 1.7])
  SetSize('thshldi',  83, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - 4, ld2radius + 2.26])
  SetSize('thshldo',  84, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - 4.15, ld2radius + 2.41])
  SetSize('vactnki',  85, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - 8, ld2radius + 6.2])
  SetSize('vactnko',  86, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - 9, ld2radius + 6.56])
  SetSize('hguide',   87, 'RCC', [1,2], [hepos - helength, heheight])
  SetSize('hguideo',  88, 'RCC', [1,2], [hepos - helength, heheight])
  SetSize('hvactnko', 89, 'RCC', [1,2,6], [d2oy + 4.7, heheight, heradius + 1.7 + 6.56])
  SetSize('hvactnki', 90, 'RCC', [1,2,6], [d2oy + 4.7, heheight, heradius + 1.7 + 6.2])
  SetSize('hvacsepo', 91, 'RCC', [1,2,6], [hepos - helength - heradius + 0.1, heheight, heradius + 1.7])
  SetSize('hvacsepi', 92, 'RCC', [1,2,6], [hepos - helength - heradius + 0.1, heheight, heradius + 1.55])
  SetSize('hthshldo', 93, 'RCC', [1,2,6], [d2oy + 7.1, heheight, heradius + 1.7 + 2.4])
  SetSize('hthshldi', 94, 'RCC', [1,2,6], [d2oy + 7.1, heheight, heradius + 1.7 + 2.25])
  SetSize('b4cshld1', 95, 'RPP', [4,5], [tgttop + lead, d2oz + 35])
  cryoy = hepos - helength/2 - 200
  SetSize('b4cshld2', 96, 'RPP', [2,3,4], [cryoy + 55, cryoy + 60, tgttop + lead])
  SetSize('pbshield', 98, 'RPP', [5], [tgttop + lead])
  SetTranslation('crtrafo', 2, 0, cryoy, heheight)

# leadthickness, d2othickness, ld2pos, ld2radius, ld2length, hepos, heradius, helength, heoffset
bounds = ((0, 20), (0, 20), (-50, 50), (0, 50), (0, 50), (-50, 50), (7.5, 40), (0, 40), (-20, 20))

constraints = ({'type': 'ineq', 'fun': lambda x: 125000 - LD2volume(x[2], x[3], x[4], x[5], x[6]) }, # LD2 volume < 125l
               {'type': 'ineq', 'fun': lambda x: 20 - abs(x[2] - x[4]/2.) }, # |ld2pos - ld2length/2| < 20cm
               {'type': 'ineq', 'fun': lambda x: x[3] - x[6] - 3.16 }, # ld2radius > inner radius
               {'type': 'ineq', 'fun': lambda x: x[5] - (x[2] - x[4]) }, # hepos > ld2pos - ld2length
               {'type': 'ineq', 'fun': lambda x: x[2] + x[3] - (x[5] + x[6] + 3.16) }, # hepos + inner radius < ld2pos + ld2radius
               {'type': 'ineq', 'fun': lambda x: x[3] - (x[6] + 3.16) - abs(x[8]) }, # heoffset < ld2radius - inner radius
               {'type': 'ineq', 'fun': lambda x: x[3] - math.sqrt((x[5] - x[2])**2 + x[8]**2) - x[6] - 3.16 }) # he inside ld2 (center distance + inner radius < ld2radius)
