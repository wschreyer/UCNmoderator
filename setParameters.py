from __future__ import print_function

import fileinput
import re
import math
import scipy.optimize

reg = '\s+([-+]?\d+(?:\.\d*)?(?:[eE][-+]?\d+)?)'

def SetSize(name, number, type, sizeindices, newsizes, inpfile, mcnpfile):
  for line in fileinput.input(inpfile, inplace = 1):
    match = re.match('\s*(\w+)\s+(\w+)'+reg, line)
    if match:
      m = list(match.groups())
      if m[1] == name:
        assert(m[0] == type)
        print(m[0] + ' ' + m[1], end = ' ')
        m = re.findall(reg, line)
        for i,size in zip(sizeindices, newsizes):
          m[i] = '{0:g}'.format(size)
        for i in m:
          print(i, end = ' ')
        print('')
      else:
        print(line, end = '')
    else:
      print(line, end = '')
  fileinput.close()

  if type == 'SPH':
    type = 'S'
  elif type == 'XZP':
    type = 'PY'
  for line in fileinput.input(mcnpfile, inplace = 1):
    match = re.match('\s*(\d+)\s+(\w+)'+reg, line)
    if match:
      m = list(match.groups())
      if int(m[0]) == number:
        assert(m[1] == type)
        print(m[0] + ' ' + m[1], end = ' ')
        m = re.findall(reg, line)
        for i,size in zip(sizeindices, newsizes):
          m[i] = '{0:g}'.format(size)
        for i in m:
          print(i, end = ' ')
        print('')
      else:
        print(line, end = '')
    else:
      print(line, end = '')
  fileinput.close()

def SetTranslation(name, number, x, y, z, inpfile, mcnpfile):
  for line in fileinput.input(inpfile, inplace = 1):
    if line.startswith('ROT-DEFI') and line.endswith(name+'\n'):
      print('ROT-DEFI  {0:40g}{1:10g}{2:10g}{3}'.format(x,y,z,name))
    else:
      print(line, end = '')

  for line in fileinput.input(mcnpfile, inplace = 1):
    match = re.match('\s*TR(\d+)'+reg+reg+reg+'(.*)', line)
    if match and int(match.group(1)) == number:
      print('TR' + match.group(1) + ' ' + '{0:g} {1:g} {2:g}'.format(x, y, z) + match.group(5))
    else:
      print(line, end = '')
      

def LD2volume(ld2offset, ld2thickness, ld2length, hepos, heradius, helength):
  innerradius = heradius + 3.16
  ld2radius = innerradius + ld2thickness
  outervol = 4./3.*ld2radius**3*math.pi + ld2radius**2*math.pi*ld2length
  innervol = 4./3.*innerradius**3*math.pi + innerradius**2*math.pi*helength
  guidevol = 10.66**2*math.pi*(ld2radius - innerradius - ld2offset + ld2length - helength)
  return outervol - innervol - guidevol

def LD2thickness(ld2offset, ld2length, hepos, heradius, helength, ld2volume):
  return scipy.optimize.brentq(lambda x: LD2volume(ld2offset, x, ld2length, hepos, heradius, helength) - ld2volume, 0.1, 30)

def SetParameters(lead, d2othickness, ld2offset, ld2thickness, ld2length, hepos, heradius, helength, heoffset, inpfile, mcnpfile):
  tgttop = 13.7
  ld2pos = hepos + ld2offset
  ld2radius = heradius + 3.16 + ld2thickness
  d2oy = ld2pos - ld2length - ld2radius - 8.5
  d2oz = tgttop + lead + d2othickness + 2*ld2radius + 2*8.46 + 10
  d2owidth = ld2radius + 8.46 + 10
  SetSize('ld2o',     51, 'RPP', [0,1,2,3,4,5], [-d2owidth, d2owidth, d2oy, ld2pos + ld2radius + 21.56, tgttop + lead + 0.3, d2oz - 0.3], inpfile, mcnpfile)
  SetSize('ld2obott', 52, 'RPP', [0,1,2,3,4,5], [-d2owidth - 0.3, d2owidth + 0.3, d2oy - 0.3, ld2pos + ld2radius + 21.86, tgttop + lead, d2oz], inpfile, mcnpfile)
  SetSize('reflecto', 53, 'RPP', [4,5], [tgttop + lead, d2oz + 30], inpfile, mcnpfile)
  SetSize('srcpit',   54, 'RPP', [4,5], [tgttop + lead, d2oz + 30], inpfile, mcnpfile)
  ld2z = tgttop + lead + d2othickness + ld2radius + 8.46
  SetSize('ld2bottl', 55, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length, ld2radius + 0.36], inpfile, mcnpfile)
  SetSize('ld2',      56, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length, ld2radius], inpfile, mcnpfile)
  heheight = ld2z + heoffset
  SetSize('ld2i',     57, 'RCC', [1,2,4,6], [hepos, heheight, -helength, heradius + 3.16], inpfile, mcnpfile)
  SetSize('ld2ibott', 58, 'RCC', [1,2,4,6], [hepos, heheight, -helength, heradius + 2.8], inpfile, mcnpfile)
  SetSize('heiibott', 59, 'RCC', [1,2,4,6], [hepos, heheight, -helength, heradius + 0.3], inpfile, mcnpfile)
  SetSize('heii',     60, 'RCC', [1,2,4,6], [hepos, heheight, -helength, heradius], inpfile, mcnpfile)
  SetSize('d2oibott', 61, 'RCC', [1,2,4,6], [ld2pos, ld2z, d2oy - 0.3 - ld2pos - 0.1, ld2radius + 7.86], inpfile, mcnpfile)
  SetSize('ld2oi',    62, 'RCC', [1,2,4,6], [ld2pos, ld2z, d2oy - ld2pos - 0.1, ld2radius + 8.16], inpfile, mcnpfile)
  SetSize('heiilow' , 63, 'SPH', [1,2,3], [hepos, heheight, heradius], inpfile, mcnpfile)
  SetSize('heiiup',   64, 'SPH', [1,2,3], [hepos - helength, heheight, heradius], inpfile, mcnpfile)
  SetSize('hebottup', 65, 'SPH', [1,2,3], [hepos - helength, heheight, heradius + 0.3], inpfile, mcnpfile)
  SetSize('hebottlo', 66, 'SPH', [1,2,3], [hepos, heheight, heradius + 0.3], inpfile, mcnpfile)
  SetSize('ld2ibolo', 67, 'SPH', [1,2,3], [hepos, heheight, heradius + 2.8], inpfile, mcnpfile)
  SetSize('ld2ilow',  68, 'SPH', [1,2,3], [hepos, heheight, heradius + 3.16], inpfile, mcnpfile)
  SetSize('ld2low',   69, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius], inpfile, mcnpfile)
  SetSize('ld2botlo', 70, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 0.36], inpfile, mcnpfile)
  SetSize('ld2iboup', 71, 'SPH', [1,2,3], [hepos - helength, heheight, heradius + 2.8], inpfile, mcnpfile)
  SetSize('ld2iup',   72, 'SPH', [1,2,3], [hepos - helength, heheight, heradius + 3.16], inpfile, mcnpfile)
  SetSize('ld2up',    73, 'SPH', [1,2,3], [ld2pos - ld2length, ld2z, ld2radius], inpfile, mcnpfile)
  SetSize('ld2botup', 74, 'SPH', [1,2,3], [ld2pos - ld2length, ld2z, ld2radius + 0.36], inpfile, mcnpfile)
  SetSize('thshldli', 75, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 2.26], inpfile, mcnpfile)
  SetSize('thshldlo', 76, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 2.41], inpfile, mcnpfile)
  SetSize('vactnkli', 77, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 6.2], inpfile, mcnpfile)
  SetSize('vactnklo', 78, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 6.56], inpfile, mcnpfile)
  SetSize('d2oibolo', 79, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 7.86], inpfile, mcnpfile)
  SetSize('d2oilow',  80, 'SPH', [1,2,3], [ld2pos, ld2z, ld2radius + 8.16], inpfile, mcnpfile)
  SetSize('vacsepli', 81, 'SPH', [1,2,3], [hepos, heheight, heradius + 1.55], inpfile, mcnpfile)
  SetSize('vacseplo', 82, 'SPH', [1,2,3], [hepos, heheight, heradius + 1.7], inpfile, mcnpfile)
  SetSize('ld2pos',   83, 'XZP', [0], [ld2pos], inpfile, mcnpfile)
  SetSize('hepos',    84, 'XZP', [0], [hepos], inpfile, mcnpfile)
  SetSize('vacsepi',  85, 'RCC', [1,2,4,6], [hepos, heheight, -helength, heradius + 1.55], inpfile, mcnpfile)
  SetSize('vacsepo',  86, 'RCC', [1,2,4,6], [hepos, heheight, -helength, heradius + 1.7], inpfile, mcnpfile)
  SetSize('vacsepui', 87, 'SPH', [1,2,3], [hepos - helength, heheight, heradius + 1.55], inpfile, mcnpfile)
  SetSize('vacsepuo', 88, 'SPH', [1,2,3], [hepos - helength, heheight, heradius + 1.7], inpfile, mcnpfile)
  SetSize('thshldi',  89, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - ld2radius - 2.26, ld2radius + 2.26], inpfile, mcnpfile)
  SetSize('thshldo',  90, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - ld2radius - 2.41, ld2radius + 2.41], inpfile, mcnpfile)
  SetSize('vactnki',  91, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - ld2radius - 6.2, ld2radius + 6.2], inpfile, mcnpfile)
  SetSize('vactnko',  92, 'RCC', [1,2,4,6], [ld2pos, ld2z, -ld2length - ld2radius - 6.56, ld2radius + 6.56], inpfile, mcnpfile)
  guidez = heheight + heradius - 7.5
  SetSize('hguide',   93, 'RCC', [1,2], [hepos - helength, guidez], inpfile, mcnpfile)
  SetSize('hguideo',  94, 'RCC', [1,2], [hepos - helength, guidez], inpfile, mcnpfile)
  SetSize('hld2i',    95, 'RCC', [1,2], [hepos - helength, guidez], inpfile, mcnpfile)
  SetSize('hld2ibot', 96, 'RCC', [1,2], [hepos - helength, guidez], inpfile, mcnpfile)
  SetSize('hvactnko', 97, 'RCC', [1,2], [d2oy + 4.7, guidez + 5.], inpfile, mcnpfile)
  SetSize('hvactnki', 98, 'RCC', [1,2], [d2oy + 4.7, guidez + 5.], inpfile, mcnpfile)
  SetSize('hvacsepo', 99, 'RCC', [1,2], [hepos - helength, guidez], inpfile, mcnpfile)
  SetSize('hvacsepi', 100,'RCC', [1,2], [hepos - helength, guidez], inpfile, mcnpfile)
  SetSize('hthshldo', 101,'RCC', [1,2], [d2oy + 7.1, guidez + 5.], inpfile, mcnpfile)
  SetSize('hthshldi', 102,'RCC', [1,2], [d2oy + 7.1, guidez + 5.], inpfile, mcnpfile)
  SetSize('b4cshld1', 103,'RPP', [4,5], [tgttop + lead, d2oz + 35], inpfile, mcnpfile)
  cryoy = hepos - helength/2 - 200
  SetSize('b4cshld2', 104,'RPP', [2,3,4], [cryoy + 55, cryoy + 60, tgttop + lead], inpfile, mcnpfile)
  SetSize('pbshield', 106,'RPP', [5], [tgttop + lead], inpfile, mcnpfile)
  SetTranslation('crtrafo', 2, 0, cryoy, guidez, inpfile, mcnpfile)
  SetTranslation('ThisTrafoDoesNotExistInFluka', 3, 0, 0, guidez, inpfile, mcnpfile)

# leadthickness, d2othickness, ld2offset, ld2length, hepos, heradius, helength, heoffset
bounds = ((0.1, 20), (0.1, 20), (-7, 7), (0.1, 25), (-20, 20), (7.5, 20), (0.1, 20), (-7, 7))

constraints = ({'type': 'ineq', 'fun': lambda x: x[3] - x[2] }, # ld2offset < ld2length
               {'type': 'ineq', 'fun': lambda x: LD2thickness(x[2],x[3],x[4],x[5],x[6],125000) - math.sqrt(min(x[2], 0)**2 + x[7]**2)}, # he inside ld2 (right center distance < ld2thickness)
               {'type': 'ineq', 'fun': lambda x: LD2thickness(x[2],x[3],x[4],x[5],x[6],125000) - math.sqrt(max(x[2] - x[3] + x[6], 0)**2 + x[7]**2)} # he inside ld2 (left center distance < ld2thickness)
              )
