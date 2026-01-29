from qiskit import QuantumCircuit, transpile
import math
import matplotlib.pyplot as plt
from qiskit_aer import Aer

# Big circuit with 5 qubits and 5 classical bits
qc = QuantumCircuit(5, 5)

# ----- SINGLE QUBIT CORE GATES -----
qc.x(0)          # X gate
qc.y(1)          # Y gate
qc.z(2)          # Z gate
qc.h(3)          # Hadamard

# ----- PHASE GATES -----
qc.s(0)
qc.t(1)
qc.sdg(2)
qc.tdg(3)

# ----- ROTATION GATES -----
qc.rx(math.pi/2, 0)
qc.ry(math.pi/3, 1)
qc.rz(math.pi/4, 2)

# ----- Multi controled rotation Gate -----
qc.mcrx(math.pi/2, [0,1], 2)
qc.mcry(math.pi/3, 2, 3)
qc.mcrz(math.pi/4, 3, 4)

# ----- CONTROLLED GATES -----
qc.cx(0, 1)                 # CNOT
qc.cy(1, 2)                 # Controlled-Y
qc.cz(2, 3)                 # Controlled-Z
qc.ch(3, 4)                 # Controlled-H

# Controlled rotations
qc.crx(math.pi/5, 0, 2)
qc.cry(math.pi/6, 1, 3)
qc.crz(math.pi/7, 2, 4)

# ----- MULTI-CONTROL GATES -----
qc.ccx(0, 1, 2)             # Toffoli (CCX)
qc.ccz(1, 2, 3)             # CCZ

# Multi-controlled X (3 controls -> target 4)
qc.mcx([0, 1, 2], 4)

# ----- SWAP FAMILY -----
qc.swap(0, 4)
qc.iswap(1, 3)
qc.cswap(2, 3, 4)           # Fredkin gate

# ----- SPECIAL HARDWARE GATES -----
qc.sx(0)
qc.sxdg(1)

# ----- RESET + MEASUREMENT -----
qc.reset(4)

qc.measure([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])

# ----- DRAW THE MONSTER -----
qc.draw("mpl")
plt.show()
sim = Aer.get_backend("aer_simulator")
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=10000).result()

print(result.get_counts())
counts = result.get_counts()
states = list(counts.keys())
values = list(counts.values())

plt.bar(states, values)
plt.xlabel("Measurement outcome (bitstring)")
plt.ylabel("Counts")
plt.title("Quantum Measurement Results")
plt.xticks(rotation=90)   # important or labels overlap 😭
plt.show()