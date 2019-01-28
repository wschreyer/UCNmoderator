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
  dir = os.environ['SCRATCH'] + '/{0}/'.format(it)
  print('iteration {0}'.format(it))
  if not os.path.isdir(dir):
    os.mkdir(dir)
    shutil.copyfile('ucn.mcnp', dir + 'ucn.mcnp')
    shutil.copyfile('ucn.inp', dir + 'ucn.inp')
    shutil.copyfile('cryostat.inp', dir + 'cryostat.inp')
    shutil.copyfile('target.inp', dir + 'target.inp')
    setParameters.SetParameters(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], dir + 'ucn.inp', dir + 'ucn.mcnp')
    jobid = subprocess.check_output(['sbatch', '-W', '-D', '.', '-o', dir + 'slurm-%j.out', 'run.sh', '{0}'.format(it)])
#      time.sleep(60)
#      subprocess.call(['python', 'mergeTallies.py'] + glob.glob(dir + 'tallies?*.root') + [dir + 'tallies.root'])
#      readme = open(dir + 'README.md', 'w')
#      subprocess.call(['python', 'writeREADME.py', dir + 'out1', dir + 'tallies.root'], stdout = readme)
#      readme.close()

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
  lossrate = 1./500.*(Q/1000.*40.)**(1.0) + 1./100. + 1./880. # 1/tau_He(Q) + 1/tau_wall + 1/tau_beta
  tau = 1./lossrate
  print('P: {0}'.format(P*40.), file = pfile)
  print('Q: {0}'.format(Q/1000.*40.), file = pfile)
  print('tau: {0}'.format(tau), file = pfile)
  print('P*tau: {0}'.format(P*40.*tau), file = pfile)

  d2ovol, graphitevol = setParameters.CalcVolume(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
  print('D2O volume: {0}'.format(d2ovol), file = pfile)
  print('Graphite volume: {0}'.format(graphitevol), file = pfile)
  # price (CAD500 per liter D2O, CAD110 per liter graphite), 230l D2O already available
  price = setParameters.CalcPrice(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
  print('Price: {0}'.format(price), file = pfile)

  pfile.close()
  if P*40.*tau > 6e8:
    return price
  else:
    return price + 6e8 - P*40.*tau

def jacPQ(p, *args):
  pool = multiprocessing.Pool()
  global iterations
  current = calcPQ(p, iterations - 1)
  h = setParameters.delta
  results = []
  for i,par in enumerate(p):
    step = list(p)
    step[i] = par + h
    results.append(pool.apply_async(calcPQ, (step, iterations + i)))
  pool.close()
  iterations = iterations + len(p)
  derivs = []
  for r in results:
    derivs.append((r.get() - current)/h)
  print(derivs)
  return derivs

pnames = ['D2Ox', 'D2Oy', 'D2Olx', 'D2Oly', 'D2Oh', 'Graphitex', 'Graphitey', 'Graphitelx', 'Graphitely', 'Graphiteh']
iterations = 0
x0 = [0, 0, 95, 125, 100, 0, 0, 140, 165, 120]
result = scipy.optimize.minimize(fun = calcPQ, x0 = x0, method = 'SLSQP', jac = jacPQ, bounds = setParameters.bounds, constraints = setParameters.constraints, tol = 0.03, options = {'disp': True, 'iprint': 1, 'eps': setParameters.delta, 'maxiter': 100, 'ftol': 0.03})
resultfile = open('result.txt', 'w')
print(result, file = resultfile)
print(result)
resultfile.close()
