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
import math
import multiprocessing

def calcPQ(p, *args):
  it = 0
  print(args)
  if len(args) == 0:
    global iterations
    it = iterations
    iterations = iterations + 1
  else:
    it = args[0]
  dir = '{0}/'.format(it)
  print('iteration {0}'.format(it))
  LD2thickness = setParameters.LD2thickness(p[2],p[3],p[4],p[5],p[6],125000)
  constraint_violated = any([constr['fun'](p) < 0 for constr in setParameters.constraints])
  if not os.path.isdir(dir):
    os.mkdir(dir)
    shutil.copyfile('ucn.mcnp', dir + 'ucn.mcnp')
    shutil.copyfile('ucn.inp', dir + 'ucn.inp')
    shutil.copyfile('cryostat.inp', dir + 'cryostat.inp')
    shutil.copyfile('target.inp', dir + 'target.inp')
    setParameters.SetParameters(p[0], p[1], p[2], LD2thickness, p[3], p[4], p[5], p[6], p[7], dir + 'ucn.inp', dir + 'ucn.mcnp')
    if not constraint_violated:
      jobid = subprocess.check_output(['sbatch', '-W', '-D', dir, 'run.sh'])
      time.sleep(60)
      subprocess.call(['python', 'mergeTallies.py'] + glob.glob(dir + 'tallies?*.root') + [dir + 'tallies.root'])
      readme = open(dir + 'README.md', 'w')
      subprocess.call(['python', 'writeREADME.py', dir + 'out1', dir + 'tallies.root'], stdout = readme)
      readme.close()

  pfile = open(dir + 'params.txt', 'w')
  for n,x in zip(pnames,p):
    print('{0}: {1}'.format(n,x), file = pfile)
  print('LD2 thickness: {0}'.format(LD2thickness), file = pfile)
  print('Constraints: {0}'.format([c['fun'](p) for c in setParameters.constraints]), file = pfile)
  print('LD2 volume: {0}'.format(setParameters.LD2volume(p[2], LD2thickness, p[3], p[4], p[5], p[6])), file = pfile)
  P = 0.
  Q = 0. # static heat load (in mW, gets multiplied by beam current, so 25 = 1W)
  tau = 0.
  if not constraint_violated:
    tallies = ROOT.TFile(dir + 'tallies.root', 'READ')
    P = readResults.GetUCNProduction(tallies)[0]
    for c in [readResults.HeIIcell, readResults.HeIIbottlecell]:
      Q = Q + readResults.GetPromptHeat(tallies, c)[0] + readResults.GetMaxDelayedHeat(tallies, c)[0]
    lossrate = 1./(1065.*(Q/1000.*40.)**(-1.0)) + 1./100. + 1./880. # 1/tau_He(Q) + 1/tau_wall + 1/tau_beta
    tau = 1./lossrate
  print('P: {0}'.format(P*40.), file = pfile)
  print('Q: {0}'.format(Q/1000.*40.), file = pfile)
  volume = 4./3.*p[5]**3*math.pi + p[5]**2*math.pi*p[6] + 125000. # total volume of converter + guides + EDM cells
  print('V: {0}'.format(volume), file = pfile)
  print('tau: {0}'.format(tau), file = pfile)
  print('P*tau/V: {0}'.format(P*40.*tau/volume), file = pfile)
  pfile.close()
  return -P*40.*tau/volume
#  if Q > 10000./40.:
#    return -P/Q/volume*100000.
#  else:
#    return -P/Q*(Q/(10000./40.))/volume*100000.

def jacPQ(p, *args):
  pool = multiprocessing.Pool()
  global iterations
  current = calcPQ(p, iterations - 1)
  h = 3.
  results = []
  for i,par in enumerate(p):
    step = list(p)
    step[i] = par + h
    results.append(pool.apply_async(calcPQ, (step, iterations + i)))
  iterations = iterations + len(p)
  derivs = []
  for r in results:
    derivs.append((r.get() - current)/h)
  print(derivs)
  return derivs

pnames = ['lead', 'd2othickness', 'ld2offset', 'ld2length', 'hepos', 'heradius', 'helength', 'heoffset']
iterations = 0
x0 = [5, 10, 0, 10, 5, 15, 10, 3]
result = scipy.optimize.minimize(fun = calcPQ, x0 = x0, method = 'SLSQP', jac = jacPQ, bounds = setParameters.bounds, constraints = setParameters.constraints, tol = 0.03, options = {'disp': True, 'iprint': 1, 'eps': 3, 'maxiter': 100, 'ftol': 0.03})
resultfile = open('result.txt', 'w')
print(result, file = resultfile)
print(result)
resultfile.close()
