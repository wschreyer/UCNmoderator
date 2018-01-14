import fileinput
import sys
import re

inc = 1.

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

for line in fileinput.input('ucn.inp', inplace = 1):
  match = re.match('\s*(RPP|RCC)\s+(\w+)'+reg+reg+reg+reg+reg+reg+'(.*)', line)
  if match:
    m = list(match.groups())
    if m[1] in ['reflecto']:
      m[7] = '{0:g}'.format(float(m[7]) + 4*inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[1] in ['ld2o', 'ld2obott', 'isovac', 'vactank']:
      m[7] = '{0:g}'.format(float(m[7]) + 4*inc)
      m[8] = '{0:g}'.format(float(m[8]) + 2*inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[1] in ['ld2bottl', 'ld2', 'ld2i', 'ld2ibott']:
      m[4] = '{0:g}'.format(float(m[4]) + inc)
      m[7] = '{0:g}'.format(float(m[7]) + 2*inc)
      m[8] = '{0:g}'.format(float(m[8]) + inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[1] in ['heii', 'heiibott']:
      m[4] = '{0:g}'.format(float(m[4]) + 2*inc)
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
    if m[0] in ['21']:
      m[7] = '{0:g}'.format(float(m[7]) + 4*inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[0] in ['20', '19', '37', '38']:
      m[7] = '{0:g}'.format(float(m[7]) + 4*inc)
      m[8] = '{0:g}'.format(float(m[8]) + 2*inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[0] in ['22', '23', '24', '25']:
      m[4] = '{0:g}'.format(float(m[4]) + inc)
      m[7] = '{0:g}'.format(float(m[7]) + 2*inc)
      m[8] = '{0:g}'.format(float(m[8]) + inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[0] in ['36', '35']:
      m[4] = '{0:g}'.format(float(m[4]) + 2*inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(line)
  else:
    sys.stdout.write(line)
fileinput.close()


