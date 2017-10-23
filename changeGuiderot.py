import fileinput
import sys
import re
import math

inc = math.radians(input('Rotate guide by how many degrees?'))

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

for line in fileinput.input('ucn.inp', inplace = 1):
  matchtrafo= re.match('\s*(ROT-DEFI)\s+' + reg + reg + reg + reg + reg + reg + '(GuideRot)', line)
  matchplane = re.match('\s*(PLA)\s+(\S+)\s+' + reg + reg + reg + reg + reg + reg, line)
  if matchplane:
    m = list(matchplane.groups())
    if m[1] == 'miter':
      m[2] = '{0:g}'.format(math.sin(inc/2.))
      m[4] = '{0:g}'.format(-math.cos(inc/2.))
    elif m[1] == 'miter2':
      m[2] = '{0:g}'.format(-math.sin(inc/2.))
      m[4] = '{0:g}'.format(math.cos(inc/2.))
    else:
      assert(false)
    for i in m:
      sys.stdout.write(i + ' ')
    sys.stdout.write('\n')
  elif matchtrafo:
    m = list(matchtrafo.groups())
    m[3] = '{0:g}'.format(math.degrees(inc))
    m[4] = '{0:g}'.format(95.*math.sin(inc))
    m[6] = '{0:g}'.format(95.*math.cos(inc))
    for i in m:
      sys.stdout.write(i + ' ')
    sys.stdout.write('\n')
  else:
    sys.stdout.write(line)
fileinput.close()

for line in fileinput.input('ucn.mcnp', inplace = 1):
  matchtrafo= re.match('\s*(\*TR2)\s+' + reg + reg + reg + reg + reg + reg + reg + reg + reg, line)
  matchplane = re.match('\s*(\d+)\s+(P)\s+' + reg + reg + reg + reg, line)
  if matchplane:
    m = list(matchplane.groups())
    if m[0] == '44':
      m[2] = '{0:g}'.format(math.sin(inc/2.))
      m[4] = '{0:g}'.format(-math.cos(inc/2.))
      m[5] = '{0:g}'.format(-95.*math.cos(inc/2))
    elif m[0] == '51':
      m[2] = '{0:g}'.format(-math.sin(inc/2.))
      m[4] = '{0:g}'.format(math.cos(inc/2.))
      m[5] = '{0:g}'.format(95.*math.cos(inc/2))
    else:
      assert(false)
    for i in m:
      sys.stdout.write(i + ' ')
    sys.stdout.write('\n')
  elif matchtrafo:
    m = list(matchtrafo.groups())
    m[4] = '{0:g}'.format(math.degrees(inc))
    m[6] = '{0:g}'.format(90 - math.degrees(inc))
    for i in m:
      sys.stdout.write(i + ' ')
    sys.stdout.write('\n')
  else:
    sys.stdout.write(line)
fileinput.close()


