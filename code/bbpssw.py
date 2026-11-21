import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from werner import werner, bell
from qiskit.quantum_info import partial_trace
import sys
from qiskit_aer.noise import NoiseModel, depolarizing_error


def ocisti(f, sum_cnot=0.0):
    rho = np.kron(werner(f), werner(f))

    vezje = QuantumCircuit(4)
    vezje.set_density_matrix(rho)

    vezje.cx(0, 2)
    vezje.cx(1, 3)
    vezje.save_density_matrix()

    model = NoiseModel()
    model.add_all_qubit_quantum_error(depolarizing_error(sum_cnot, 2), ["cx"])

    simulator = AerSimulator(method="density_matrix", noise_model=model)

    rezultat = simulator.run(vezje).result()
    rho = np.asarray(rezultat.data(0)["density_matrix"])

    # obdrzimo izida 00 in 11 na drugem paru
    p = np.kron(np.diag([1, 0, 0, 1]), np.eye(4))
    uspeh = float(np.real(np.trace(p @ rho)))

    # stanje po uspesni meritvi
    rho_uspeh = p @ rho @ p

    # odstranimo drugi par in normaliziramo stanje
    rho_izhod = partial_trace(rho_uspeh, [2, 3]).data / uspeh

    f_izhod = float(np.real(np.vdot(bell, rho_izhod @ bell)))

    return f_izhod, uspeh


if __name__ == "__main__":
    f = float(sys.argv[1]) if len(sys.argv) > 1 else 0.8
    sum_cnot = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0

    f_izhod, uspeh = ocisti(f, sum_cnot)

    print("Zacetna zvestoba:", f)
    print("Sum CNOT:", sum_cnot)
    print("Verjetnost uspeha:", round(uspeh, 6))
    print("Izhodna zvestoba:", round(f_izhod, 6))
    print("Izboljsanje:", round(f_izhod - f, 6))
    print("Parov na izhod:", round(2 / uspeh, 4))

    a = (1 - f) / 3

    p_teorija = f**2 + 2*f*a + 5*a**2
    f_teorija = (f**2 + a**2) / p_teorija

    if sum_cnot == 0:
        print("Teoreticna zvestoba:", round(f_teorija, 6))
        print("Razlika:", round(abs(f_izhod - f_teorija), 10))

        assert np.isclose(f_izhod, f_teorija)
        assert np.isclose(uspeh, p_teorija)