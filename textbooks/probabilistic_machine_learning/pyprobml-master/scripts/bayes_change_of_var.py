# Based on https://github.com/probml/pmtk3/blob/master/demos/bayesChangeOfVar.m
# MC on change of variables and empirical distribution, highlighting that
# modes are not, in general, preserved.

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os
from pyprobml_utils import save_fig

# Ensure stochastic reproducibility.
np.random.seed(42)
    
# Define a mapping from x-space to y-space.
def ginv(x):
    """transform func"""
    return 1 / (1 + np.exp(5 - x))

# Define a probability density on x-space, and sample from it.
mu = 6
sigma = 1
n = 10 ** 6
x_samples = norm.rvs(size=n, loc=mu, scale=sigma)

# Calculate a histogram for the samples in x-space and a histogram
# for their transformations to y-space.
hist_x, bin_edges_x = np.histogram(x_samples, bins=50, density=True)
hist_y, bin_edges_y = np.histogram(ginv(x_samples), bins=50, density=True)

# Plot the histograms, the mapping function, and an indication of how
# the x-distribution's mean maps to y-space.
linewidth = 5
plt.bar(bin_edges_x[:-1], hist_x, color='red', align='edge', width=bin_edges_x[1] - bin_edges_x[0])
plt.barh(bin_edges_y[:-1], hist_y, color='green', align='edge', height=bin_edges_y[1] - bin_edges_y[0])
x_range = np.arange(0, 10, 0.01)
plt.plot(x_range, ginv(x_range), 'blue', linewidth=linewidth)
plt.vlines(mu, ymin=0, ymax=ginv(mu), color='yellow', linewidth=linewidth)
plt.hlines(ginv(mu), xmin=0, xmax=mu, color='yellow', linewidth=linewidth)
plt.text(9, 1/10, r'$p_X$');
plt.text(2/3, 2/10, r'$p_Y$');
plt.text(9, ginv(9) - 1/10, r'$g$');

## Save the figure.
save_fig('bayesChangeOfVar.pdf')
plt.show()

