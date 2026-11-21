import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import partial_trace
from werner import werner, bell

f = 0.8

rho = np.kron(werner(f), werner(f))

vezje = QuantumCircuit(4)
vezje.set_density_matrix(rho)
vezje.save_density_matrix()

simulator = AerSimulator(method="density_matrix")
rezultat = simulator.run(vezje).result()
stanje = rezultat.data(0)["density_matrix"]

par1 = partial_trace(stanje, [2, 3])
par2 = partial_trace(stanje, [0, 1])

f1 = float(np.real(np.vdot(bell, par1.data @ bell)))
f2 = float(np.real(np.vdot(bell, par2.data @ bell)))

print("Stevilo kubitov:", vezje.num_qubits)
print("Zvestoba prvega para:", round(f1, 6))
print("Zvestoba drugega para:", round(f2, 6))