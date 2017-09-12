import fileinput
import sys
import re

#inc = float(raw_input('Increase D2O thickness by '))
inc = 1.

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'

for line in fileinput.input('ucn.inp', inplace = 1):
  match = re.match('\s*(RPP|RCC)\s+(\w+)'+reg+reg+reg+reg+reg+reg+reg+'?', line)
  if match:
    m = list(match.groups())
    if m[1] in ['boxInn']:
      m[7] = '{0:g}'.format(float(m[7]) + inc)
      for i in m:
        if i != None:
          sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[1] in ['ld2o', 'ld2obott', 'reflecto', 'ld2bottl', 'ld2', 'ld2i', 'ld2ibott', 'heiibott', 'heii', 'isovac', 'vactank']:
      if m[0] == 'RCC':
        m[4] = '{0:g}'.format(float(m[4]) + inc)
      elif m[0] == 'RPP':
        m[6] = '{0:g}'.format(float(m[6]) + inc)
        m[7] = '{0:g}'.format(float(m[7]) + inc)
      for i in m:
        if i != None:
          sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(line)
  else:
    sys.stdout.write(line)
fileinput.close()

for line in fileinput.input('ucn.mcnp', inplace = 1):
  match = re.match('\s*(\d+)\s+(RPP|RCC)'+reg+reg+reg+reg+reg+reg+reg+'?', line)
  if match:
    m = list(match.groups())
    if m[0] in ['18']:
      m[7] = '{0:g}'.format(float(m[7]) + inc)
      for i in m:
        if i != None:
          sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    elif m[0] in ['19', '20', '21', '22', '23', '24', '25', '35', '36', '37', '38']:
      if m[1] == 'RCC':
        m[4] = '{0:g}'.format(float(m[4]) + inc)
      elif m[1] == 'RPP':
        m[6] = '{0:g}'.format(float(m[6]) + inc)
        m[7] = '{0:g}'.format(float(m[7]) + inc)
      for i in m:
        if i != None:
          sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(line)
  else:
    sys.stdout.write(line)
fileinput.close()


