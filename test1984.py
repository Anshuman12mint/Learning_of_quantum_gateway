from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

target_number = 37
n_qubits = 7
iterations = 8

target_bin = format(target_number, '07b')

qc = QuantumCircuit(n_qubits, n_qubits)

# Superposition
for i in range(n_qubits):
    qc.h(i)

# Grover iterations
for _ in range(iterations):

    # Oracle
    for i, bit in enumerate(target_bin):
        if bit == '0':
            qc.x(i)

    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)

    for i, bit in enumerate(target_bin):
        if bit == '0':
            qc.x(i)

    # Diffusion
    for i in range(n_qubits):
        qc.h(i)
        qc.x(i)

    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)

    for i in range(n_qubits):
        qc.x(i)
        qc.h(i)

# Measure
qc.measure(range(n_qubits), range(n_qubits))

sim = Aer.get_backend("aer_simulator")
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1000).result()

counts = result.get_counts()
print(counts)