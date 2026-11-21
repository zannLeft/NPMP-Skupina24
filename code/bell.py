
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

vezje = QuantumCircuit(2)
vezje.h(0)
vezje.cx(0, 1)
vezje.save_density_matrix()

simulator = AerSimulator(method="density_matrix")
rezultat = simulator.run(vezje).result()
rho = np.asarray(rezultat.data(0)["density_matrix"])

bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
zvestoba = float(np.real(np.vdot(bell, rho @ bell)))

print("Zvestoba:", round(zvestoba, 6))

assert np.isclose(zvestoba, 1.0)
print("test working")