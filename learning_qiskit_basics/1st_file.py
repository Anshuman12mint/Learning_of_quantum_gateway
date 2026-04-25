import qiskit as qk
from matplotlib import pyplot as plt
from qiskit_aer import Aer
from qiskit import transpile
from qiskit.visualization import plot_circuit_layout




qc = qk.QuantumCircuit(2,2)


qc.s(0)
qc.measure([0,1],[0,1])




qc.draw("mpl")
plt.show()




print(qc)
sim = Aer.get_backend("aer_simulator")
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1000).result()




print(result.get_counts())



