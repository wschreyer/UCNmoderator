import fileinput
import sys
import subprocess

for line in fileinput.input('ucn.inp', inplace = 1):
  columns = line[15:].split(' ')
  if line.startswith('RPP reflecto   '):
     columns[5] = '{0:f}'.format(float(columns[5]) + 2)
     sys.stdout.write(line[0:14])
     for column in columns:
       sys.stdout.write(' ' + column)
     sys.stdout.write('\n')
  elif line.startswith('RCC ld2obott   ') \
  or line.startswith('RCC ld2bottl   ') \
  or line.startswith('RCC ld2        ') \
  or line.startswith('RCC ld2i       ') \
  or line.startswith('RCC ld2ibott   ') \
  or line.startswith('RCC heiibott   ') \
  or line.startswith('RCC heii       ') \
  or line.startswith('RCC isovac     ') \
  or line.startswith('RCC vactank    '):
     columns[5] = '{0:g}'.format(float(columns[5]) + 2)
     sys.stdout.write(line[0:14])
     for column in columns:
       sys.stdout.write(' ' + column)
  else:
    sys.stdout.write(line)
fileinput.close()

for line in fileinput.input('README.md', inplace = 1):
  if fileinput.filelineno() == 14 and line.startswith('LD2: '):
    sys.stdout.write('{0}{1:.0f}{2}'.format(line[0:5], float(line[5:7]) + 2, line[7:]))
  elif fileinput.filelineno() == 15 and line.startswith('He-II: '):
    sys.stdout.write('{0}{1:.0f}{2}'.format(line[0:7], float(line[7:9]) + 2, line[9:]))
  else:
    sys.stdout.write(line)
fileinput.close()

subprocess.call("./qsub.sh")
