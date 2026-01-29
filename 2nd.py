from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector
import numpy as np
from qiskit_aer import Aer

# parameters (symbolic angles)
θ1 = Parameter('θ1')
θ2 = Parameter('θ2')
θ3 = Parameter('θ3')

# build a parameterized variational circuit
qc = QuantumCircuit(3, 3)

# layer 1 — superposition
qc.h(0)
qc.h(1)
qc.h(2)

# entanglement chain
qc.cx(0, 1)
qc.cx(1, 2)

# parameterized rotations
qc.ry(θ1, 0)
qc.rz(θ2, 1)
qc.rx(θ3, 2)

# more entanglement
qc.cz(0, 2)

# inverse layer (uncomputation style)
qc.cx(1, 2)
qc.cx(0, 1)

# bind actual numeric values to parameters
bound_qc = qc.assign_parameters({
    θ1: np.pi / 3,
    θ2: np.pi / 5,
    θ3: np.pi / 7
})

# simulate full quantum state (no measurement yet)
state = Statevector.from_instruction(bound_qc)

print("STATEVECTOR:")
print(state)

# now measure everything
bound_qc.measure([0,1,2], [0,1,2])

# run on simulator
sim = Aer.get_backend("aer_simulator")
compiled = transpile(bound_qc, sim, optimization_level=3)
result = sim.run(compiled, shots=2048).result()

print("\nMEASUREMENT COUNTS:")
print(result.get_counts())

print("\nFINAL CIRCUIT:")
print(bound_qc)
