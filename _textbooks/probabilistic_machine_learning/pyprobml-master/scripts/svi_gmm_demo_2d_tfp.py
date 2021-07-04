# SVI for a mixture of 3 Gaussians in 2d
# https://github.com/brendanhasz/svi-gaussian-mixture-model/blob/master/BayesianGaussianMixtureModel.ipynb


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions

import svi_gmm_model_tfp as GMM


import numpy as np
import matplotlib.pyplot as plt
import os
figdir = "../figures"
def save_fig(fname): plt.savefig(os.path.join(figdir, fname))

# Random seed
np.random.seed(12345)
tf.random.set_seed(12345)

# Generate some data
N = 3000
X = np.random.randn(N, 2).astype('float32')
X[:1000, :] += [2, 0]
X[1000:2000, :] -= [2, 4]
X[2000:, :] += [-2, 4]

# Plot the data
plt.figure()
plt.plot(X[:, 0], X[:, 1], '.')
plt.axis('equal')
save_fig('svi_gmm_2d_data.pdf')
plt.show()

# Make a TensorFlow Dataset from that data
batch_size = 500
dataset = tf.data.Dataset.from_tensor_slices(
    (X)).shuffle(10000).batch(batch_size)

# A GMM with 3 components in 2 dimensions
model = GMM.GaussianMixtureModel(3, 2)

nepochs = 1000
model.fit(dataset, N, nepochs)

# Compute log likelihood at each point on a grid
Np = 100 #number of grid points
Xp, Yp = np.meshgrid(np.linspace(-6, 6, Np), np.linspace(-6, 6, Np))
Pp = np.column_stack([Xp.flatten(), Yp.flatten()]).astype('float32')
Z, _ = model(Pp, sampling=False)
Z = np.reshape(Z, (Np, Np))
        
# Show the fit mixture density
plt.figure()
plt.imshow(np.exp(Z),
           extent=(-6, 6, -6, 6),
           origin='lower')
cbar = plt.colorbar()
cbar.ax.set_ylabel('Likelihood')
save_fig('svi_gmm_2d_fit.pdf')
plt.show()



# Sample from the mean variational posterior
means = tfd.Normal(model.locs, model.scales).sample(10000)

# Plot the mean samples for a single 
plt.figure()
sns.kdeplot(means[:, 0, 0].numpy(),
            means[:, 0, 1].numpy(),
            n_levels=10)
save_fig('svi_gmm_2d_post_mean_comp0.pdf')
plt.show()

