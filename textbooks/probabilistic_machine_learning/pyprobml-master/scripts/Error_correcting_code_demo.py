# Illustrate parity check code using a directed graphical model
# Authors: murphyk@, Drishtii@
# Based on
#https://github.com/probml/pmtk3/blob/master/demos/errorCorrectingCodeDemo.m

#!pip install pgmpy
import pyprobml_utils as pml
import pgmpy_utils as pgm
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import numpy as np
import matplotlib.pyplot as plt

# DAG structure
model = BayesianModel([ ('X2', 'X3'), ('X1', 'X3'), ('X1', 'Y1'), ('X2', 'Y2'), ('X3', 'Y3')])

# Defining individual CPDs.
CPDs = {}
CPDs['X1'] = TabularCPD(variable='X1', variable_card=2, values=[[0.5], [0.5]])

CPDs['X2'] = TabularCPD(variable='X2', variable_card=2, values=[[0.5], [0.5]])

CPDs['X3'] = TabularCPD(variable='X3', variable_card=2,
                   values=[[1, 0, 0, 1], [0, 1, 1, 0]],
                  evidence=['X1', 'X2'],
                  evidence_card=[2, 2])

noise = 0.2
for i in range(3):
    parent = 'X{}'.format(i + 1)
    child = 'Y{}'.format(i + 1)
    CPDs[child] = TabularCPD(variable=child, variable_card=2,
                   values=[[1-noise, noise], [noise, 1-noise]],
                  evidence=[parent],
                  evidence_card=[2])

# Make model
for cpd in CPDs.values():
    model.add_cpds(cpd)
model.check_model()

from pgmpy.inference import VariableElimination
infer = VariableElimination(model)

# Inference
evidence = {'Y1': 1, 'Y2': 0, 'Y3': 0}
marginals = {}
for i in range(3):
    name = 'X{}'.format(i+1)
    post= infer.query([name],  evidence=evidence).values
    marginals[name] = post
print(marginals)

joint = infer.query(['X1','X2','X3'], evidence=evidence).values
J = joint.reshape(8)
fig, ax = plt.subplots()
plt.title('p(x|y=1,0,0)')
y = ['0' ,'000', '001', '010', '011', '100', '101', '110', '111']
ax.bar(x = np.arange(8), height=J)
ax.set_xticklabels(y, rotation = 90) 
pml.savesfig('error_correcting.pdf')
plt.savefig('error_correcting.pdf')
plt.show()

pgm.visualize_model(model)
