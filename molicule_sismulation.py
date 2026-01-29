import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import Estimator
from scipy.optimize import minimize

# --- 1. Hydrogen molecule Hamiltonian (precomputed for bond length ~0.74 Å) ---
H = SparsePauliOp.from_list([
    ("II", -1.052373245772859),
    ("ZI",  0.39793742484318045),
    ("IZ", -0.39793742484318045),
    ("ZZ", -0.01128010425623538),
    ("XX",  0.18093119978423156),
])

# --- 2. Ansatz (trainable quantum circuit) ---
params = ParameterVector("θ", 8)

qc = QuantumCircuit(2)
qc.ry(params[0], 0)
qc.ry(params[1], 1)
qc.cx(0, 1)

# --- 3. Estimator (quantum expectation engine) ---
estimator = Estimator()

def energy(theta):
    job = estimator.run(
        circuits=[qc],
        observables=[H],
        parameter_values=[theta]
    )
    return job.result().values[0]

# --- 4. Classical optimizer ---
init = np.random.random(2)

res = minimize(energy, init, method="COBYLA")

print("\n🔥 H₂ MOLECULE SIMULATION RESULT 🔥")
print("Ground-state energy:", res.fun)
print("Optimal parameters:", res.x)
