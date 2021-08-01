# jeffreys prior for bernoulli using 2 paramterizatiobs
# fig 1.9 of 'Bayeysian Modeling and Computation'

import numpy as np
import matplotlib.pyplot as plt 
import pyprobml_utils as pml

θ = np.linspace(0, 1, 100)
κ = (θ / (1-θ))
y = 2
n = 7

_, ax = plt.subplots(2, 2, figsize=(10, 5),
                     sharex='col', sharey='row')

ax[0, 0].set_title("Jeffreys' prior for Alice")
ax[0, 0].plot(θ, θ**(-0.5) * (1-θ)**(-0.5))
ax[1, 0].set_title("Jeffreys' posterior for Alice")
ax[1, 0].plot(θ, θ**(y-0.5) * (1-θ)**(n-y-0.5))
ax[1, 0].set_xlabel("θ")
ax[0, 1].set_title("Jeffreys' prior for Bob")
ax[0, 1].plot(κ, κ**(-0.5) * (1 + κ)**(-1))
ax[1, 1].set_title("Jeffreys' posterior for Bob")
ax[1, 1].plot(κ, κ**(y-0.5) * (1 + κ)**(-n-1))
ax[1, 1].set_xlim(-0.5, 10)
ax[1, 1].set_xlabel(r'$\phi$')
ax[1, 1].text(-4.0, 0.030, size=18, s=r'$p(\theta \mid x) \, \frac{d\theta}{d\phi}$')
ax[1, 1].annotate("", xy=(-0.5, 0.025), xytext=(-4.5, 0.025),
                  arrowprops=dict(facecolor='black', shrink=0.05))
ax[1, 1].text(-4.0, 0.007, size=18, s= r'$p(\phi \mid x) \, \frac{d\phi}{d\theta}$')
ax[1, 1].annotate("", xy=(-4.5, 0.015), xytext=(-0.5, 0.015),
                  arrowprops=dict(facecolor='black', shrink=0.05),
                  annotation_clip=False)

plt.subplots_adjust(wspace=0.4, hspace=0.4)
plt.tight_layout()
pml.save_fig("jeffreys_priors.pdf", dpi=300)