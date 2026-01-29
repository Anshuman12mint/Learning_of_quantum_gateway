from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit import transpile

qc = QuantumCircuit(2, 2)

# --- Step 1: Superposition (all 4 states at once) ---
qc.h(0)
qc.h(1)

# --- Step 2: Oracle (mark |11⟩ by flipping its phase) ---
qc.cz(0, 1)   # flips phase ONLY when both are 1 😈

# --- Step 3: Diffusion (interference amplifier) ---
qc.h(0)
qc.h(1)

qc.z(0)
qc.z(1)

qc.cz(0, 1)

qc.h(0)
qc.h(1)

# --- Step 4: Measure ---
qc.measure([0, 1], [0, 1])

# Run
sim = Aer.get_backend("aer_simulator")
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1000).result()

print(qc)
print(result.get_counts())
