"""Esqueleto comum aos algoritmos de consulta: H -> oráculo -> H -> medição."""

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def compile_circuit(function: QuantumCircuit) -> QuantumCircuit:
    """Circuito com phase kickback (Deutsch, Deutsch-Jozsa, Bernstein-Vazirani).

    O oráculo tem n qubits de entrada e 1 de saída. A saída é preparada em |->.
    """
    n = function.num_qubits - 1

    qc = QuantumCircuit(n + 1, n)

    qc.x(n)  # Flipa o qubit n para 1
    qc.h(range(n + 1))  # Hadamard em todos (|+> |+> ... |->)

    qc.barrier()
    # inplace=False retornaria um novo qc
    qc.compose(function, inplace=True)  # qubits mapeados para o mesmo índice
    qc.barrier()

    qc.h(range(n))
    qc.measure(range(n), range(n))

    return qc


def sample(qc: QuantumCircuit, shots: int = 1024) -> dict[str, int]:
    """Executa o circuito no simulador e devolve as contagens.

    As chaves estão em little-endian: o bit 0 é o caractere mais à direita.
    """
    result = StatevectorSampler().run([qc], shots=shots).result()
    # "c" é o nome padrão do registrador clássico criado por QuantumCircuit(q, c)
    return result[0].data.c.get_counts()


def measure_once(qc: QuantumCircuit) -> str:
    """Uma única execução; devolve a string medida."""
    return next(iter(sample(qc, shots=1)))
