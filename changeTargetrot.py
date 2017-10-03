import fileinput
import sys
import re
import math

inc = math.radians(-15.)

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

for line in fileinput.input('ucn.inp', inplace = 1):
  matchbeam = re.match('(BEAMPOS)\s+' + reg + reg + reg + reg, line)
  matchtrafo= re.match('(ROT-DEFI)\s+' + reg + reg + reg + '(.*)', line)
  if matchbeam:
    m = list(matchbeam.groups())
    x = float(m[1])
    z = float(m[3])
    m[1] = '{0:g}'.format(x*math.cos(inc) - z*math.sin(inc))
    m[3] = '{0:g}'.format(z*math.cos(inc) + x*math.sin(inc))
    m[4] = '{0:g}'.format(math.cos(math.acos(float(m[4])) + inc))
    for i in m:
      sys.stdout.write(i + ' ')
    sys.stdout.write('\n')
  elif matchtrafo:
    m = list(matchtrafo.groups())
    m[3] = '{0:g}'.format(float(m[3]) + math.degrees(inc))
    for i in m:
      sys.stdout.write(i + ' ')
    sys.stdout.write('\n')
  else:
    sys.stdout.write(line)
fileinput.close()

for line in fileinput.input('ucn.mcnp', inplace = 1):
  match = re.match('(TR1)\s+' + reg + reg + reg + reg + reg + reg + reg + reg + reg, line)
  if match:
    m = list(match.groups())
    m[4] = '{0:g}'.format(math.cos(math.acos(float(m[4])) - inc))
    m[6] = '{0:g}'.format(math.cos(-math.acos(float(m[6])) + inc))
    for i in m:
      sys.stdout.write(i + ' ')
    sys.stdout.write('\n')
  else:
    sys.stdout.write(line)
fileinput.close()


