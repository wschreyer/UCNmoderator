import fileinput
import sys
import re

#inc = float(raw_input('Move target by '))
inc = 5.

offset = 0.0
for line in fileinput.input('ucn.inp', inplace = 1):
  match = re.match('\$start_translat ([-+]?\d+) ([-+]?\d+) ([-+]?\d+)', line)
  if match:
    offset = float(match.group(1)) + inc
    sys.stdout.write('$start_translat {0:.0f} {1} {2}\n'.format(offset, match.group(2), match.group(3)))
  else:
    sys.stdout.write(line)
fileinput.close()

for line in fileinput.input('README.md', inplace = 1):
  if line.startswith('Cylindrical D2O (300K), LD2 (20 or 80K?), and He-II vessels offset from target by '):
    sys.stdout.write('Cylindrical D2O (300K), LD2 (20 or 80K?), and He-II vessels offset from target by {0:.0f}cm.\n'.format(offset))
  else:
    sys.stdout.write(line)
fileinput.close()

