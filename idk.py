import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import Estimator
from scipy.optimize import minimize

# --- Hamiltonian ---
H = SparsePauliOp.from_list([
    ("ZZ", 1.0),
    ("XI", 0.5),
    ("IX", 0.5)
])

# --- Parameterized circuit ---
params = ParameterVector("θ", 2)

qc = QuantumCircuit(2)
qc.ry(params[0], 0)
qc.ry(params[1], 1)
qc.cx(0, 1)

# --- Estimator ---
estimator = Estimator()

def energy(theta):
    # Estimator wants LISTS
    job = estimator.run(
        circuits=[qc],
        observables=[H],
        parameter_values=[theta]
    )
    result = job.result()
    return result.values[0]

# --- Classical optimizer (COBYLA) ---
init = np.random.random(2)

res = minimize(energy, init, method="COBYLA")

print("\n🔥 OPTIMIZATION DONE 🔥")
print("Minimum energy:", res.fun)
print("Best parameters:", res.x)
