import fileinput
import sys
import re

inc = 5.

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

for line in fileinput.input('ucn.inp', inplace = 1):
  match = re.match('\s*(RPP|RCC)\s+(\w+)'+reg+reg+reg+reg+reg+reg+'(.*)', line)
  if match:
    m = list(match.groups())
    if m[1] in ['target1', 'target2', 'target3', 'target4', 'target5', \
                'target1c', 'target2c', 'target3c', 'target4c', 'target5c', \
                'targetw', 'xitwin1', 'tgtcasei', 'tgtcaseo', 'beamo', 'beami']:
      m[2] = '{0:g}'.format(float(m[2]) + inc)
      if m[0] == 'RPP':
        m[3] = '{0:g}'.format(float(m[3]) + inc)
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
    if m[0] in ['1', '2', '3', '4', '5', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']:
      m[2] = '{0:g}'.format(float(m[2]) + inc)
      if m[1] == 'RPP':
        m[3] = '{0:g}'.format(float(m[3]) + inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(line)
  else:
    sys.stdout.write(line)
fileinput.close()


