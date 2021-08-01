# inference for UGM by autodiff
# we consider a length 3 HMM with K states
# h1 - h2 - h3

import numpy as np # original numpy
import jax.numpy as jnp
from jax import grad, jit, vmap
from jax.ops import index, index_add, index_update
from functools import partial

K = 2
nnodes = 3
edges = [ [0,1], [1,2]]
nedges = len(edges)
np.random.seed(0)
nodePots = []
nodePotsLog = []
for i in range(nnodes):
    nodePot = np.random.rand(K)
    nodePots.append(nodePot)
    nodePotsLog.append(np.log(nodePot))
edgePots = []
edgePotsLog = []
for i in range(nedges):
    edgePot = np.random.rand(K,K)
    edgePots.append(edgePot)
    edgePotsLog.append(np.log(edgePot))
    
def compute_joint(nodePots, edgePots):    
    joint = np.ones((K, K, K))
    np0 = nodePots[0].reshape((K,1,1))
    joint = joint * np0
    np1 = nodePots[1].reshape((1,K,1))
    joint = joint * np1
    np2 = nodePots[2].reshape((1,1,K))
    joint = joint * np2
    ep0 = edgePots[0].reshape((K,K,1))
    joint = joint * ep0
    ep1 = edgePots[1].reshape((1,K,K))
    joint = joint * ep1
    return joint

joint = compute_joint(nodePots, edgePots)

'''
# sanity check
x = [0,1,0]
p = 1
for i in range(nnodes):
    p = p * nodePots[i][x[i]]
for i, e in enumerate(edges):
    src = e[0]
    sink = e[1]
    p = p * edgePots[i][x[src], x[sink]] 
j = joint[x[0], x[1], x[2]]
assert p == j
#assert(joint[0,1,0] == nodePots[0][0] * nodePots[1][1] * nodePots[2][0])
'''

# Compute marginals by brute force
Z = np.sum(joint)
jointNorm = joint / Z
marg0 = np.sum(jointNorm, (1, 2))
marg1 = np.sum(jointNorm, (0, 2))
marg2 = np.sum(jointNorm, (0, 1))

# Now use autodiff!

def compute_Z(nodePots):
    factors = [nodePots[0], nodePots[1], nodePots[2], edgePots[0], edgePots[1]]
    str = 'A,B,C, AB,BC'
    Z = jnp.einsum(str, *factors)
    return Z

ZZ = np.float(compute_Z(nodePots))
assert np.isclose(Z, ZZ)

# Computes A(eta), where A=logZ and eta=logPot
def compute_logZ(nodePotsLog):
    nodePots = []
    for i in range(len(nodePotsLog)):
        nodePots.append(jnp.exp(nodePotsLog[i]))
    return jnp.log(compute_Z(nodePots))

#gg = grad(jnp.log())
g = grad(compute_logZ)(nodePotsLog)
margProbs = []
for i in range(nnodes):
    margProbs.append(np.array(g[i]))

assert np.allclose(margProbs[0], marg0)
assert np.allclose(margProbs[1], marg1)
assert np.allclose(margProbs[2], marg2)

# Super short version
logZ_fun = lambda logpots: jnp.log(jnp.einsum('A,B,C,AB,BC', *[jnp.exp(lp) for lp in logpots]))
logpots = nodePotsLog + edgePotsLog
logZ = logZ_fun(logpots)
assert np.isclose(logZ, np.log(Z))
probs = grad(logZ_fun)(logpots)
