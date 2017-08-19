import fileinput
import sys
import subprocess

inc = float(raw_input('Change radius by '))

for line in fileinput.input('ucn.inp', inplace = 1):
  columns = line[15:].split(' ')
  if line.startswith('RCC ld2o       ') \
  or line.startswith('RCC ld2obott   ') \
  or line.startswith('RCC ld2bottl   ') \
  or line.startswith('RCC ld2        ') \
  or line.startswith('RCC ld2i       ') \
  or line.startswith('RCC ld2ibott   ') \
  or line.startswith('RCC heiibott   ') \
  or line.startswith('RCC heii       ') \
  or line.startswith('RCC isovac     ') \
  or line.startswith('RCC vactank    '):
    columns[6] = '{0:g}'.format(float(columns[6]) + inc)
    sys.stdout.write(line[0:14])
    for column in columns:
      sys.stdout.write(' ' + column)
    sys.stdout.write('\n')
  else:
    sys.stdout.write(line)

  if line.startswith('RCC heii       '):
    heii_radius = columns[6]

fileinput.close()

for line in fileinput.input('README.md', inplace = 1):
  if fileinput.filelineno() == 13 and line.startswith('D2O: '):
    sys.stdout.write('{0}{1:.0f}\n'.format(line[0:8], float(line[8:]) + inc))
  elif fileinput.filelineno() == 14 and line.startswith('LD2: '):
    sys.stdout.write('{0}{1:.0f}\n'.format(line[0:9], float(line[9:]) + inc))
  elif fileinput.filelineno() == 15 and line.startswith('He-II: '):
    sys.stdout.write('{0}{1:.0f}\n'.format(line[0:11], float(line[11:]) + inc))
  else:
    sys.stdout.write(line)
fileinput.close()

subprocess.call(['./qsub.sh', '{0}'.format(heii_radius)])
