import numpy as np
import matplotlib.pyplot as plt
import pyprobml_utils as pml

np.random.seed(seed=1)

class Prior():
    def __init__(self, alpha1, beta1, alpha2, beta2):
        self.alpha1 = alpha1
        self.beta1 = beta1
        self.alpha2 = alpha2
        self.beta2 = beta2
        
class Net():
    def __init__(self, net_type, nin, nhidden, nout, nwts, outfunc, 
                 alpha1=None, beta1=None, alpha2=None, beta2=None, w1=None, b1=None, w2=None, b2=None):
        self.net_type = net_type
        self.nin = nin
        self.nhidden = nhidden
        self.nout = nout
        self.nwts = nwts
        self.alpha1 = alpha1
        self.beta1 = beta1
        self.alpha2 = alpha2
        self.beta2 = beta2
        self.w1 = w1
        self.b1 = b1
        self.w2 = w2
        self.b2 = b2        
        outfns = ['linear', 'logistic', 'softmax']
        if outfunc in outfns:
            self.outfunc = outfunc
        else:
            raise ValueError('Undefined output function. Exiting.')

def MLP(nin, nhidden, nout, outfunc, prior):
    net_type = 'mlp'
    nwts = (nin+1)*nhidden + (nhidden+1)*nout
    net = Net(net_type, nin, nhidden, nout, nwts, outfunc)
    net.alpha1 = prior.alpha1
    net.beta1 = prior.beta1
    net.alpha2 = prior.alpha2
    net.beta2 = prior.beta2
    net.w1  = prior.alpha1 * np.random.randn(nin, nhidden)
    net.b1 = prior.beta1 * np.random.randn(1, nhidden)
    net.w2 = prior.alpha2 * np.random.randn(nhidden, nout)
    net.b2 = prior.beta2 * np.random.randn(1, nout)
    return net
    
    
def MLP_fwd(net, xvals_t):
    ndata = xvals_t.shape[0]
    z = np.tanh(xvals_t.reshape(-1, 1).dot(net.w1) + np.ones((ndata, 1)).dot(net.b1))
    a = z.dot(net.w2) + np.ones((ndata, 1)).dot(net.b2)
    
    if net.outfunc == 'linear':
        y = a
    elif net.outfunc == 'logistic':
        maxcut = -np.log(np.finfo(float).eps)
        mincut = -np.log(1/np.finfo(float).tiny-1)
        a = min(a, maxcut)
        a = max(a, mincut)
        y = 1/(1 + np.exp(-a))
    elif net.outfunc == 'softmax':
        maxcut = np.log(float('inf'))-np.log(net.nout)
        mincut = np.log(np.finfo(float).tiny)
        a = min(a, maxcut)
        a = max(a, mincut)
        temp = np.exp(a)
        y = temp/(np.sum(temp, 1).dot(np.ones(1, net.nout)))
    else:
        raise ValueError('Unknown activation function')
        
    return y, a, z


params0 = np.array([5, 1, 1, 1])
params = np.tile(params0, (5, 1))
sf = 5

params[1, 0] = params0[0] * sf
params[2, 1] = params0[1] * sf
params[3, 2] = params0[2] * sf
params[4, 3] = params0[3] * sf

ntrials = 4

for t in range(ntrials):
    alpha1 = params[t, 0]
    alpha2 = params[t, 2]
    beta1 = params[t, 1]
    beta2 = params[t, 3]
    
    nhidden = 12
    nout = 1
    prior = Prior(alpha1, beta1, alpha2, beta2)
    xvals = np.arange(-1, 1.005, 0.005)
    nsample = 10
    
    fig = plt.figure(figsize=(10, 7))
    
    for i in range(nsample):
        net = MLP(1, nhidden, 1, 'linear', prior)
        yvals, _, _ = MLP_fwd(net, xvals.T)
        plt.plot(xvals.T, yvals, color='k', lw=2)
        plt.ylim([-10, 10])
        ttl = r'$\alpha_1 = {},\; \beta_1 = {},\; \alpha_2 = {},\; \beta_2 = {}$'.format(
            alpha1, beta1, alpha2, beta2)
        plt.title(ttl, fontsize=18)
    plt.show()
    pml.save_fig(f'mlpPriors-{t}.pdf', dpi=300)
        
                 