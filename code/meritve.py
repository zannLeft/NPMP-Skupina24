import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from werner import werner
from bbpssw import ocisti
import csv
from pathlib import Path

f = 0.8
sum_cnot = 0.05

_, p_natancno = ocisti(f, sum_cnot)

rho = np.kron(werner(f), werner(f))

vezje = QuantumCircuit(4, 2)
vezje.set_density_matrix(rho)

vezje.cx(0, 2)
vezje.cx(1, 3)
vezje.measure([2, 3], [0, 1])

model = NoiseModel()
model.add_all_qubit_quantum_error(depolarizing_error(sum_cnot, 2), ["cx"])

simulator = AerSimulator(method="density_matrix", noise_model=model)

print("Natancna verjetnost uspeha:", round(p_natancno, 6))


rezultati = []

for shots in [1024, 4096, 16384]:
    ocene = []

    for seme in range(30):
        rezultat = simulator.run(vezje, shots=shots, seed_simulator=seme).result()
        stevci = rezultat.get_counts()

        sprejeti = stevci.get("00", 0) + stevci.get("11", 0)
        p_ocena = sprejeti / shots

        ocene.append(p_ocena)

        rezultati.append({
            "shots": shots,
            "seme": seme,
            "p_ocena": p_ocena,
            "p_natancno": p_natancno
        })

    povprecje = np.mean(ocene)
    odklon = np.std(ocene, ddof=1)
    odklon_teorija = np.sqrt(p_natancno * (1 - p_natancno) / shots)

    print(f"{shots} meritev:")
    print("  Povprecje:", round(povprecje, 6))
    print("  Standardni odklon:", round(odklon, 6))
    print("  Teoreticni odklon:", round(odklon_teorija, 6))

pot = Path(__file__).resolve().parent.parent / "results"

with open(pot / "meritve.csv", "w", newline="", encoding="utf-8") as datoteka:
    zapis = csv.DictWriter(datoteka, fieldnames=rezultati[0].keys())
    zapis.writeheader()
    zapis.writerows(rezultati)