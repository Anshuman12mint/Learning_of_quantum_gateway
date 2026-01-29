from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import math

# --- Prepare initial state ---
qc1 = QuantumCircuit(1)
qc1.ry(0.8, 0)
original = Statevector.from_instruction(qc1)

# --- Teleportation circuit ---
qc = QuantumCircuit(3, 2)

qc.ry(0.8, 0)

qc.h(1)
qc.cx(1, 2)

qc.cx(0, 1)
qc.h(0)

qc.measure(0, 0)
qc.measure(1, 1)

qc.cx(1, 2)
qc.cz(0, 2)

final = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))

print("ORIGINAL STATE:")
print(original)

print("\nFINAL STATE ON QUBIT 2:")
print(final.partial_trace([0,1]))
