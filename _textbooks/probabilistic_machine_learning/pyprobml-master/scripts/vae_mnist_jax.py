# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A basic variational autoencoder (VAE) on binarized MNIST using Numpy and JAX.

This file uses the stax network definition library and the optimizers
optimization library.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

import matplotlib.pyplot as plt

import jax.numpy as np
from jax.config import config
from jax import jit, grad, lax, random
from jax.experimental import optimizers
from jax.experimental import stax
from jax.experimental.stax import Dense, FanOut, Relu, Softplus
from examples import datasets


def gaussian_kl(mu, sigmasq):
  """KL divergence from a diagonal Gaussian to the standard Gaussian."""
  return -0.5 * np.sum(1. + np.log(sigmasq) - mu**2. - sigmasq)

def gaussian_sample(rng, mu, sigmasq):
  """Sample a diagonal Gaussian."""
  return mu + np.sqrt(sigmasq) * random.normal(rng, mu.shape)

def bernoulli_logpdf(logits, x):
  """Bernoulli log pdf of data x given logits."""
  return -np.sum(np.logaddexp(0., np.where(x, -1., 1.) * logits))

def elbo(rng, params, images):
  """Monte Carlo estimate of the negative evidence lower bound."""
  enc_params, dec_params = params
  mu_z, sigmasq_z = encode(enc_params, images)
  logits_x = decode(dec_params, gaussian_sample(rng, mu_z, sigmasq_z))
  return bernoulli_logpdf(logits_x, images) - gaussian_kl(mu_z, sigmasq_z)


latent_size = 20
image_nrows = 28
image_ncols = 28
image_size = image_nrows * image_ncols

def image_sample(rng, params, nrow, ncol):
  """Sample images from the generative model."""
  _, dec_params = params
  code_rng, img_rng = random.split(rng)
  logits = decode(dec_params, random.normal(code_rng, (nrow * ncol, latent_size)))
  sampled_images = random.bernoulli(img_rng, np.logaddexp(0., logits))
  return image_grid(nrow, ncol, sampled_images, (image_nrows, image_ncols))

def image_grid(nrow, ncol, imagevecs, imshape):
  """Reshape a stack of image vectors into an image grid for plotting."""
  images = iter(imagevecs.reshape((-1,) + imshape))
  return np.vstack([np.hstack([next(images).T for _ in range(ncol)][::-1])
                    for _ in range(nrow)]).T



encoder_init, encode = stax.serial(
    Dense(512), Relu,
    Dense(512), Relu,
    FanOut(2),
    stax.parallel(Dense(latent_size), stax.serial(Dense(latent_size), Softplus)),
)

decoder_init, decode = stax.serial(
    Dense(512), Relu,
    Dense(512), Relu,
    Dense(image_size),
)


if __name__ == "__main__":
  step_size = 0.001
  num_epochs = 50
  batch_size = 32
  hidden_size = 20
  nrow, ncol = 10, 10  # sampled image grid size

  test_rng = random.PRNGKey(1)  # fixed prng key for evaluation
  #imfile = os.path.join(os.getenv("TMPDIR", "/tmp/"), "mnist_vae_{:03d}.png")
  path = os.environ["PYPROBML"]
  figdir = os.path.join(path, "figures")
  imfile = os.path.join(figdir, "mnist_vae_{:03d}.png")
  
  # labels are not used
  train_images, _, test_images, _ = datasets.mnist(permute_train=True)
  num_complete_batches, leftover = divmod(train_images.shape[0], batch_size)
  num_batches = num_complete_batches + bool(leftover)

  enc_init_rng, dec_init_rng = random.split(random.PRNGKey(2))
  _, init_encoder_params = encoder_init(enc_init_rng, (batch_size, image_size))
  _, init_decoder_params = decoder_init(dec_init_rng, (batch_size, latent_size))
  init_params = init_encoder_params, init_decoder_params

  opt_init, opt_update, get_params = optimizers.momentum(step_size, mass=0.9)

  def binarize_batch(rng, i, images):
    i = i % num_batches
    batch = lax.dynamic_slice_in_dim(images, i * batch_size, batch_size)
    return random.bernoulli(rng, batch)

  @jit
  def run_epoch(rng, opt_state):
    def body_fun(i, opt_state):
      elbo_rng, data_rng = random.split(random.fold_in(rng, i))
      batch = binarize_batch(data_rng, i, train_images)
      loss = lambda params: -elbo(elbo_rng, params, batch) / batch_size
      g = grad(loss)(get_params(opt_state))
      return opt_update(i, g, opt_state)
    return lax.fori_loop(0, num_batches, body_fun, opt_state)

  @jit
  def evaluate(opt_state, images):
    params = get_params(opt_state)
    elbo_rng, data_rng, image_rng = random.split(test_rng, 3)
    binarized_test = random.bernoulli(data_rng, images)
    test_elbo = elbo(elbo_rng, params, binarized_test) / images.shape[0]
    sampled_images = image_sample(image_rng, params, nrow, ncol)
    return test_elbo, sampled_images

  opt_state = opt_init(init_params)
  for epoch in range(num_epochs):
    tic = time.time()
    opt_state = run_epoch(random.PRNGKey(epoch), opt_state)
    test_elbo, sampled_images = evaluate(opt_state, test_images)
    print("{: 3d} {} ({:.3f} sec)".format(epoch, test_elbo, time.time() - tic))
    plt.imsave(imfile.format(epoch), sampled_images, cmap=plt.cm.gray)
