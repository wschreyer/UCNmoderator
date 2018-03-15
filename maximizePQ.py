from __future__ import print_function
import scipy.optimize
import setParameters
import readResults
import subprocess
import os
import shutil
import ROOT
import time
import glob

def calcPQ(p, *args):
  LD2thickness = setParameters.LD2thickness(p[2],p[3],p[4],14.7,200000)
  setParameters.SetParameters(p[0], p[1], p[2], LD2thickness, p[3], p[4], 14.7, 10.8, p[5])
  dir = '{0}/'.format(iterations)
  global iterations
  print('iteration {0}'.format(iterations))
  iterations = iterations + 1
  if not os.path.isdir(dir):
    os.mkdir(dir)
    shutil.copyfile('ucn.mcnp', dir + 'ucn.mcnp')
    shutil.copyfile('ucn.inp', dir + 'ucn.inp')
    shutil.copyfile('cryostat.inp', dir + 'cryostat.inp')
    shutil.copyfile('target.inp', dir + 'target.inp')
    jobid = subprocess.check_output(['sbatch', '-W', '-D', dir,'-a', '1-50', 'run.sh'])
    
    subprocess.call(['python', 'mergeTallies.py'] + glob.glob('/home/wschreye/scratch/mcnpsims/*.root'))
    shutil.copyfile('tallies.root', dir + 'tallies.root')
    readme = open(dir + 'README.md', 'w')
    subprocess.call(['python', 'writeREADME.py'], stdout = readme)
    readme.close()
  tallies = ROOT.TFile(dir + 'tallies.root', 'READ')
  P = readResults.GetUCNProduction(tallies)[0]
  Q = 0.
  for c in [readResults.HeIIcell, readResults.HeIIbottlecell]:
    Q = Q + readResults.GetPromptHeat(tallies, c)[0] + readResults.GetMaxDelayedHeat(tallies, c)[0]
  pfile = open(dir + 'params.txt', 'w')
  for n,x in zip(pnames,p):
    print('{0}: {1}'.format(n,x), file = pfile)
  print('LD2 thickness: {0}'.format(LD2thickness), file = pfile)
  print('Constraints: {0}'.format([c['fun'](p) for c in setParameters.constraints]), file = pfile)
  print('LD2 volume: {0}'.format(setParameters.LD2volume(p[2], LD2thickness, p[3], p[4], 14.7)), file = pfile)
  print('P/Q: {0}'.format(P/Q), file = pfile)
  print('P: {0}'.format(P), file = pfile)
  print('Q: {0}'.format(Q), file = pfile)
  pfile.close()
  if Q > 5000./40.:
    return -P/Q
  else:
    return -P/Q*(Q/(5000./40.))

pnames = ['lead', 'd2othickness', 'ld2offset', 'ld2length', 'hepos', 'heoffset']
iterations = 0
x0 = [5, 10, 0, 30, 3, 3]
result = scipy.optimize.minimize(fun = calcPQ, x0 = x0, method = 'SLSQP', bounds = setParameters.bounds, constraints = setParameters.constraints, tol = 0.03, options = {'disp': True, 'iprint': 1, 'eps': 3, 'maxiter': 100, 'ftol': 0.03})
resultfile = open('result.txt', 'w')
print(result, file = resultfile)
print(result)
resultfile.close()
