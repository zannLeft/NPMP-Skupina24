from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

vezje = QuantumCircuit(4, 2)

vezje.cx(0, 2)
vezje.cx(1, 3)
vezje.measure([2, 3], [0, 1])

simulator = AerSimulator(method="density_matrix")
prevedeno = transpile(vezje, simulator, optimization_level=1)


def izpisi(naslov, qc):
    dvokubitna = sum(1 for ukaz in qc.data if ukaz.operation.num_qubits == 2)

    print(naslov)
    print("  Stevilo kubitov:", qc.num_qubits)
    print("  Globina vezja:", qc.depth())
    print("  Dvokubitna vrata:", dvokubitna)
    print("  Operacije:", dict(qc.count_ops()))


izpisi("Pred transpilingom:", vezje)
izpisi("Po transpilingu:", prevedeno)