import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import Estimator
from scipy.optimize import minimize

# --- Ansatz (same for all distances) ---
params = ParameterVector("θ", 2)

qc = QuantumCircuit(2)
qc.ry(params[0], 0)
qc.ry(params[1], 1)
qc.cx(0, 1)

estimator = Estimator()

def vqe_energy(H):
    def energy(theta):
        job = estimator.run(
            circuits=[qc],
            observables=[H],
            parameter_values=[theta]
        )
        return job.result().values[0]

    init = np.random.random(2)
    res = minimize(energy, init, method="COBYLA")
    return res.fun

# --- Precomputed Hamiltonians for different bond distances ---
# (Normally computed via quantum chemistry packages; hardcoded here)
hamiltonians = {
    0.3: SparsePauliOp.from_list([
        ("II", -0.8), ("ZI", 0.6), ("IZ", -0.6), ("ZZ", -0.2), ("XX", 0.15)
    ]),
    0.5: SparsePauliOp.from_list([
        ("II", -1.0), ("ZI", 0.45), ("IZ", -0.45), ("ZZ", -0.1), ("XX", 0.17)
    ]),
    0.7: SparsePauliOp.from_list([
        ("II", -1.05), ("ZI", 0.40), ("IZ", -0.40), ("ZZ", -0.01), ("XX", 0.18)
    ]),
    1.0: SparsePauliOp.from_list([
        ("II", -1.02), ("ZI", 0.35), ("IZ", -0.35), ("ZZ", 0.05), ("XX", 0.16)
    ]),
    1.5: SparsePauliOp.from_list([
        ("II", -0.9), ("ZI", 0.25), ("IZ", -0.25), ("ZZ", 0.12), ("XX", 0.10)
    ])
}

distances = []
energies = []

print("Running quantum simulations...\n")

for R, H in hamiltonians.items():
    E = vqe_energy(H)
    distances.append(R)
    energies.append(E)
    print(f"Bond length {R} Å → Energy {E:.4f}")

# --- Plot energy curve ---
plt.plot(distances, energies, marker="o")
plt.xlabel("Bond distance (Å)")
plt.ylabel("Energy (Hartree)")
plt.title("H₂ Potential Energy Curve (Quantum Simulation)")
plt.grid(True)
plt.show()
