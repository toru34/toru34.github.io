'''
Author : Srikar reddy Jilugu(@always-newbie161)
This code is referenced from
https://github.com/probml/pmtk3/blob/master/demos/sparseDictDemo.m
spams package is from
https://gitlab.inria.fr/thoth/spams-devel
(Can be instaled from PyPi through pip install ...)
'''

import numpy as np
from spams import trainDL, nmf, displayPatches, im2col_sliding
from sklearn.decomposition import TruncatedSVD
from PIL import Image
import matplotlib.pyplot as plt
import pyprobml_utils as pml

# dimension of latent space or no .of basis vectors.
D = 64
img = Image.open('../data/lena.png')
img = np.array(img) / 255
# spams accepts only column stored arrays i.e fortran-based
X = np.asfortranarray(img)
# preprocessing the image with a sliding window to get the actual observational data.
X = im2col_sliding(X, 12, 12)
print('Shape of observational data: ',X.shape)
print('Shape of the matrix of basis vectors will be: ',(X.shape[0],D))

methods = ['pca', 'spca', 'dl', 'nmf']

for m in methods:

    # Some preprocess should be done before training.
    # nmf - unitnorm
    # spca, dl - centered and unit norm
    # pca - centered data will be SVD decomposed.

    X_m = X

    # NMf accepts onlt non-negative data, So it should not be centered.
    if m != 'nmf':
        X_m = X_m - X_m.mean(axis=0)

    # normalizing..
    X_m = np.asfortranarray(X_m / np.sqrt((X_m * X_m).sum(axis=0)), dtype=np.float64)

    if m == 'pca':
        svd = TruncatedSVD(n_components=D, n_iter=7)
        W = svd.fit_transform(X_m)
    else:
        param = {'K': D, 'numThreads': -1, 'batchsize': 256,
                 'iter': 1000}

        if m == 'nmf':
            W = nmf(X_m, **param)
        else:
            param['verbose'] = False
            if m == 'spca':
                param['lambda1'] = 0.1
                param['gamma1'] = 0.1
                param['modeD'] = 1
                W = trainDL(X_m, **param)
            elif m == 'dl':
                param['lambda1'] = 0.1
                param['mode'] = 2
                W = trainDL(X_m, **param)

    # resulting basisvectors will be visualized as image patches.
    img = displayPatches(W)
    img = np.uint8(img[:, :, 0] * 255.)
    img = Image.fromarray(img, mode='L')
    plt.title('sparse_dict_demo_{}'.format(m))
    plt.imshow(img, cmap='gray')
    pml.savefig('sparse_dict_demo_{}.pdf'.format(m))
    plt.show()
