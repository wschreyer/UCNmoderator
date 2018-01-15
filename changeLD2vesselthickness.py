import fileinput
import sys
import re

inc = 0.5

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

for line in fileinput.input('ucn.inp', inplace = 1):
  match = re.match('\s*(RPP|RCC)\s+(\w+)'+reg+reg+reg+reg+reg+reg+'(.*)', line)
  if match:
    m = list(match.groups())
    if m[1] in ['ld2bottl']:
      m[4] = '{0:g}'.format(float(m[4]) - inc)
      m[7] = '{0:g}'.format(float(m[7]) + 2*inc)
      m[8] = '{0:g}'.format(float(m[8]) + inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[1] in ['ld2ibott']:
      m[4] = '{0:g}'.format(float(m[4]) + inc)
      m[7] = '{0:g}'.format(float(m[7]) - 2*inc)
      m[8] = '{0:g}'.format(float(m[8]) - inc)
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
    if m[0] in ['22']:
      m[4] = '{0:g}'.format(float(m[4]) - inc)
      m[7] = '{0:g}'.format(float(m[7]) + 2*inc)
      m[8] = '{0:g}'.format(float(m[8]) + inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[0] in ['25']:
      m[4] = '{0:g}'.format(float(m[4]) + inc)
      m[7] = '{0:g}'.format(float(m[7]) - 2*inc)
      m[8] = '{0:g}'.format(float(m[8]) - inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(line)
  else:
    sys.stdout.write(line)
fileinput.close()


