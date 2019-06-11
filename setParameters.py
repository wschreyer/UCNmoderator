from __future__ import print_function

import fileinput
import re
import math
import scipy.optimize
import random

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'

delta = -10.

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
    if line.startswith('ROT-DEFI') and line.endswith(name+'\n'):
      print('ROT-DEFI  {0:40g}{1:10g}{2:10g}{3}'.format(x,y,z,name))
    else:
      print(line, end = '')

  for line in fileinput.input(mcnpfile, inplace = 1):
    match = re.match('\s*TR(\d+)'+reg+reg+reg+'(.*)', line)
    if match and int(match.group(1)) == number:
      print('TR' + match.group(1) + ' ' + '{0:g} {1:g} {2:g}'.format(x, y, z) + match.group(5))
    else:
      print(line, end = '')
      
def CalcVolume(d2ox, d2oy, d2olx, d2oly, d2oh, graphitex, graphitey, graphitelx, graphitely, graphiteh):
  tgttop = 13.8
  d2olowx = d2ox - d2olx/2
  d2ohix = d2ox + d2olx/2
  d2olowy = d2oy - d2oly/2
  d2ohiy = d2oy + d2oly/2
  glowx = graphitex - graphitelx/2
  ghix = graphitex + graphitelx/2
  glowy = graphitey - graphitely/2
  ghiy = graphitey + graphitely/2
  vhit = 0
  d2ohit = 0
  d2ovhit = 0
  ghit = 0
  total = 1000000
  for i in range(0, total):
    x = random.uniform(min(d2olowx, glowx), max(d2ohix, ghix))
    y = random.uniform(min(d2olowy, glowy), max(d2ohiy, ghiy))
    z = random.uniform(tgttop, tgttop + max(d2oh, graphiteh))
    if -5.9 < y < 5.9 and x**2 + (z - 61.86)**2 < 40.3**2: # hit straight part of vac tank
      vhit = vhit + 1
    elif y < -5.9 and x**2 + (y + 5.9)**2 + (z - 61.86)**2 < 40.3**2: # hit vac tank downstream
      vhit = vhit + 1
    elif 5.9 < y and x**2 + (y - 5.9)**2 + (z - 61.86)**2 < 40.3**2: # hit vac tank upstream
      vhit = vhit + 1
    elif y < -5.9 and x**2 + (z - 79.96)**2 < 16.5**2: # hit horizontal penetration of vac tank
      vhit = vhit + 1
    elif d2olowx < x < d2ohix and d2olowy < y < d2ohiy and tgttop < z < tgttop + d2oh: # hit D2O
      d2ohit = d2ohit + 1
    elif d2olowx - 0.6 < x < d2ohix + 0.6 and d2olowy - 0.6 < y < d2ohiy + 0.6 and tgttop < z < tgttop + d2oh + 1.2: # hit d2o vessel
      d2ovhit = d2ovhit + 1
    elif glowx < x < ghix and glowy < y < ghiy and tgttop < z < tgttop + graphiteh: # hit graphite
      ghit = ghit + 1

  vol = (max(d2ohix, ghix) - min(d2olowx, glowx))*(max(d2ohiy, ghiy) - min(d2olowy, glowy))*max(d2oh, graphiteh)
  return float(d2ohit)/total*vol, float(ghit)/total*vol

def CalcPrice(d2ox, d2oy, d2olx, d2oly, d2oh, graphitex, graphitey, graphitelx, graphitely, graphiteh):
  d2ovol, graphitevol = CalcVolume(d2ox, d2oy, d2olx, d2oly, d2oh, graphitex, graphitey, graphitelx, graphitely, graphiteh)
  # 500CAD/l D2O, 110CAD/l graphite, assume that we can reuse 230l of D2O but none of the too small/custom graphite blocks
  return max(0, (d2ovol - 430000)*0.5 + (graphitevol)*0.11)

def jacPrice(p):
  current = CalcPrice(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
  stepped = []
  for i,par in enumerate(p):
    step = list(p)
    step[i] = par + delta
    stepped.append(CalcPrice(step[0], step[1], step[2], step[3], step[4], step[5], step[6], step[7], step[8], step[9]))
  return [(s - current)/delta for s in stepped]

def SetParameters(d2ox, d2oy, d2olx, d2oly, d2oh, graphitex, graphitey, graphitelx, graphitely, graphiteh, inpfile, mcnpfile):
  tgttop = 18.
  d2olowx = d2ox - d2olx/2
  d2ohix = d2ox + d2olx/2
  d2olowy = d2oy - d2oly/2
  d2ohiy = d2oy + d2oly/2
  glowx = graphitex - graphitelx/2
  ghix = graphitex + graphitelx/2
  glowy = graphitey - graphitely/2
  ghiy = graphitey + graphitely/2
  SetSize('ld2o',     51, 'RPP', [0,1,2,3,5], [d2olowx, d2ohix, d2olowy, d2ohiy, tgttop + 0.6 + d2oh], inpfile, mcnpfile)
  SetSize('ld2obott', 52, 'RPP', [0,1,2,3,5], [d2olowx - 0.6, d2ohix + 0.6, d2olowy - 0.6, d2ohiy + 0.6, tgttop + d2oh + 1.2], inpfile, mcnpfile)
  SetSize('ld2osep',  53, 'RPP', [0,1,2,3,4,5], [d2olowx - 0.6, d2ohix + 0.6, d2olowy - 0.6, d2ohiy + 0.5, tgttop + 0.3 + d2oh/2., tgttop + 0.9 + d2oh/2.], inpfile, mcnpfile)
  SetSize('reflecto', 54, 'RPP', [0,1,2,3,5], [glowx, ghix, glowy, ghiy, tgttop + graphiteh], inpfile, mcnpfile)
  SetSize('srcpit',   55, 'RPP', [0,1,2,3,5], [glowx, ghix, glowy, ghiy, tgttop + graphiteh], inpfile, mcnpfile)
  SetSize('hd2obott',111, 'RCC', [4], [d2olowy + 5.9 - 0.6], inpfile, mcnpfile)
  SetSize('hd2oi',   112, 'RCC', [4], [d2olowy + 5.9 - 0.6], inpfile, mcnpfile)
  SetSize('b4cshld1',113, 'RPP', [0,1,2,3,5], [min(d2olowx,glowx) - 5, max(d2ohix, ghix) + 5, min(d2olowy, glowy) - 5, max(d2ohiy, ghiy) + 5, tgttop + max(d2oh, graphiteh) + 5], inpfile, mcnpfile)

bounds = ((-10, 10), (-10, 10), (50, 150), (50, 150), (20, 150), (-10, 10), (-10, 10), (50, 200), (50, 200), (20, 200))

constraints = (
#        {'type': 'eq', 'fun': lambda x: CalcPrice(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9]) - 200000, 'jac': lambda x: jacPrice(x)}
  )
              
              
