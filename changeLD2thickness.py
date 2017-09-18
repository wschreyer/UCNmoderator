import fileinput
import sys
import re

#inc = float(raw_input('Increase D2O thickness by '))
inc = 1.

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

for line in fileinput.input('ucn.inp', inplace = 1):
  match = re.match('\s*(RPP|RCC)\s+(\w+)'+reg+reg+reg+reg+reg+reg+'(.*)', line)
  if match:
    m = list(match.groups())
    if m[1] in ['ld2o', 'ld2obott', 'reflecto', 'ld2bottl', 'ld2', 'isovac', 'vactank']:
      m[7] = '{0:g}'.format(float(m[7]) + inc) # increase zmax
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[1] in ['ld2i', 'ld2ibott', 'heiibott', 'heii']:
      assert(m[0] == 'RCC')
      m[4] = '{0:g}'.format(float(m[4]) + inc) # increase zmin
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(line)
  else:
    sys.stdout.write(line)
fileinput.close()

for line in fileinput.input('ucn.mcnp', inplace = 1):
  match = re.match('\s*(\d+)\s+(RPP|RCC)'+reg+reg+reg+reg+reg+reg+'(.*)', line)
  if match:
    m = list(match.groups())
    if m[0] in ['19', '20', '21', '22', '23', '37', '38']:
      m[7] = '{0:g}'.format(float(m[7]) + inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[0] in ['24', '25', '35', '36']:
      assert(m[1] == 'RCC')
      m[4] = '{0:g}'.format(float(m[4]) + inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(line)
  else:
    sys.stdout.write(line)
fileinput.close()


