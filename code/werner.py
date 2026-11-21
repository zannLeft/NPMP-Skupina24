import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
p = np.outer(bell, bell.conj())

def werner(f):
    return f * p + (1 - f) / 3 * (np.eye(4) - p)


if __name__ == "__main__":
    f = 0.8

    vezje = QuantumCircuit(2)
    vezje.set_density_matrix(werner(f))
    vezje.save_density_matrix()

    simulator = AerSimulator(method="density_matrix")
    rezultat = simulator.run(vezje).result()
    rho = np.asarray(rezultat.data(0)["density_matrix"])

    zvestoba = float(np.real(np.vdot(bell, rho @ bell)))

    print("Zacetna zvestoba:", f)
    print("Izracunana zvestoba:", round(zvestoba, 6))
