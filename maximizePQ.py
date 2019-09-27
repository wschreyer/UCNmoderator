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

def calcPQ(p, dir):
  pfile = open(dir + 'params.txt', 'w')
  for n,x in zip(pnames,p):
    print('{0}: {1}'.format(n,x), file = pfile)
  P = 0.
  Q = 0. # static heat load (in mW, gets multiplied by beam current, so 25 = 1W)
  tau = 0.
  tallies = ROOT.TFile(dir + 'tallies.root', 'READ')
  P = readResults.GetUCNProduction(tallies)[0]
  for c in [readResults.HeIIcell, readResults.HeIIbottlecell]:
    Q = Q + readResults.GetPromptHeat(tallies, c)[0] + readResults.GetMaxDelayedHeat(tallies, c)[0]
  lossrate = 1./(500.*(Q/1000.*40.)**(-1.0)) + 1./100. + 1./880. # 1/tau_He(Q) + 1/tau_wall + 1/tau_beta
  tau = 1./lossrate
  print('P: {0}'.format(P*40.), file = pfile)
  print('Q: {0}'.format(Q/1000.*40.), file = pfile)
  print('tau: {0}'.format(tau), file = pfile)
  print('P*tau: {0}'.format(P*40.*tau), file = pfile)
  pfile.close()
  return -P*40.*tau
#  if Q > 10000./40.:
#    return -P/Q/volume*100000.
#  else:
#    return -P/Q*(Q/(10000./40.))/volume*100000.

def runjob(p, *args):
  it = 0
  print(args)
  if len(args) == 0:
    global iterations
    it = iterations
    iterations = iterations + 1
  else:
    it = args[0]
  dir = os.environ['SCRATCH'] + '/{0}/'.format(it)
  print('iteration {0}'.format(it))
  if not os.path.isdir(dir):
    os.mkdir(dir)
    shutil.copyfile('ucn.mcnp', dir + 'ucn.mcnp')
    shutil.copyfile('ucn.inp', dir + 'ucn.inp')
    shutil.copyfile('cryostat.inp', dir + 'cryostat.inp')
    shutil.copyfile('target.inp', dir + 'target.inp')
    setParameters.SetParameters(p[0], p[1], dir + 'target.inp', dir + 'ucn.mcnp')
#    jobid = subprocess.check_output(['sbatch', '-W', '-D', '.', '-o', dir + 'slurm-%j.out', 'run.sh', '{0}'.format(it)])
    jobid = subprocess.check_output(['sbatch', '-D', '.', '-o', dir + 'slurm-%j.out', 'run.sh', '{0}'.format(it)])
  return calcPQ(p, dir)


def jacPQ(p, *args):
  pool = multiprocessing.Pool()
  global iterations
  current = calcPQ(p, iterations - 1)
  h = -5.
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

ROOT.gROOT.SetBatch(1)
pnames = ['xoffset', 'yoffset']
iterations = 0
for x in range(-25,30,5):
  for y in range(-25,30,5):
    runjob([x,y], iterations)
    iterations = iterations + 1
#x0 = [0, 0]
#result = scipy.optimize.minimize(fun = calcPQ, x0 = x0, method = 'SLSQP', jac = jacPQ, bounds = setParameters.bounds, tol = 0.03, options = {'disp': True, 'iprint': 1, 'eps': 3, 'maxiter': 100, 'ftol': 0.03})
#resultfile = open('result.txt', 'w')
#print(result, file = resultfile)
#print(result)
#resultfile.close()
