"""Simon: descobrir s em f(x) = f(y) <=> y ∈ {x, x ⊕ s}."""

from qiskit import QuantumCircuit

from .circuitos import sample


def simon_circuit(function: QuantumCircuit) -> QuantumCircuit:
    """H -> oráculo -> H, medindo só o registrador de entrada.

    O oráculo tem n qubits de entrada e n de saída. A saída começa em |0...0>
    (sem phase kickback): o oráculo escreve f(x) nela e emaranha os registradores.
    """
    n = function.num_qubits // 2

    qc = QuantumCircuit(2 * n, n)

    qc.h(range(n))

    qc.barrier()
    qc.compose(function, inplace=True)  # qubits mapeados para o mesmo índice
    qc.barrier()

    qc.h(range(n))
    qc.measure(range(n), range(n))

    return qc


def simon_query(s: str) -> QuantumCircuit:
    """Oráculo 2-para-1 com f(x) = f(x ⊕ s).

    f(x) = x        se x_i = 0
    f(x) = x ⊕ s    se x_i = 1   (i = algum índice com s_i = 1)
    """
    n = len(s)
    qc = QuantumCircuit(2 * n)

    # Camada 1: copia x para a saída -> |x>|0> vira |x>|x>
    for j in range(n):
        qc.cx(j, n + j)

    # Posições dos bits 1 de s (reversed: bit 0 é o caractere mais à direita)
    ones = [j for j, bit in enumerate(reversed(s)) if bit == "1"]

    if not ones:  # s = 000...0: f(x) = x já é injetora
        return qc

    i = ones[0]  # um índice qualquer com s_i = 1

    # Camada 2: se x_i = 1, faz XOR de s inteiro na saída
    for j in ones:
        qc.cx(i, n + j)  # controle SEMPRE em i; o alvo percorre os bits 1 de s

    return qc


def dot_mod2(a: str, b: str) -> int:
    """Produto escalar mod 2 entre duas strings de bits do mesmo tamanho."""
    return sum(x == "1" and y == "1" for x, y in zip(a, b)) % 2


def find_s(counts: dict, n: int) -> list[str]:
    """Candidatos s != 0 que satisfazem y · s = 0 para todo y medido.

    Uma lista com um único elemento significa s encontrado; com vários, faltam
    medidas independentes.
    """
    candidates = []

    for k in range(1, 2**n):
        candidate = f"{k:0{n}b}"

        if all(dot_mod2(candidate, v) == 0 for v in counts):
            candidates.append(candidate)

    return candidates


def simon_algorithm(function: QuantumCircuit, shots: int = 1024) -> list[str]:
    """Executa o circuito de Simon e devolve os candidatos a s."""
    n = function.num_qubits // 2
    counts = sample(simon_circuit(function), shots=shots)
    return find_s(counts, n)
