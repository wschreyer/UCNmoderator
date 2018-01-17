import fileinput
import sys
import re

inc = 5.

reg = '\s*([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)\s+'

for line in fileinput.input('ucn.mcnp', inplace = 1):
  match = re.match('\s*(M\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', line)
  if match:
    m = list(match.groups())
    if m[0] in ['M43']:
      m[2] = '{0:g}'.format(float(m[2]) - inc)
      m[4] = '{0:g}'.format(float(m[4]) + inc)
      for i in m:
        sys.stdout.write(i+' ')
      sys.stdout.write('\n')
    else:
      sys.stdout.write(line)
  else:
    sys.stdout.write(line)
fileinput.close()


