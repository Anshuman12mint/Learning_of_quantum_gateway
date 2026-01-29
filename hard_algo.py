import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

qc = QuantumCircuit(2)

qc.h([0,1])
qc.cz(0,1)
qc.h([0,1])

qc.z([0,1])

qc.cz(0,1)

qc.h([0,1])

qc.measure_all()
qc.draw("mpl")
plt.show()

sim = Aer.get_backend("aer_simulator")
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1000).result()

print(result.get_counts())

