from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
import math


from qiskit_aer import Aer


qc = QuantumCircuit(3, 2)


# --- Step 0: Prepare an UNKNOWN quantum state on qubit 0 ---
qc.ry(0.8, 0)   # secret state 😈


print("Initial state (to teleport):")
print(Statevector.from_instruction(qc))


# --- Step 1: Create entanglement between qubit 1 and 2 ---
qc.h(1)
qc.cx(1, 2)


# --- Step 2: Bell measurement on qubit 0 and 1 ---
qc.cx(0, 1)
qc.h(0)


# --- Step 3: Measure qubit 0 and 1 (DESTROYS ORIGINAL) ---
qc.measure(0, 0)
qc.measure(1, 1)


# --- Step 4: Classical correction on Bob's qubit (qubit 2) ---
qc.cx(1, 2)
qc.cz(0, 2)


# Draw the circuit
print("\nTeleportation Circuit:")
print(qc)


sim = Aer.get_backend("aer_simulator")
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=10000).result()


print(result.get_counts())