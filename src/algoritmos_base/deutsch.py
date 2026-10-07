"""Deutsch e Deutsch-Jozsa: f é constante ou balanceada?"""

import numpy as np
from qiskit import QuantumCircuit

from .circuitos import compile_circuit, measure_once


def deutsch_function(case: int) -> QuantumCircuit:
    """Oráculo de uma das 4 funções f: {0,1} -> {0,1}.

    1 -> f(0), f(1) = 0, 0   (constante)
    2 -> f(0), f(1) = 0, 1   (balanceada)
    3 -> f(0), f(1) = 1, 0   (balanceada)
    4 -> f(0), f(1) = 1, 1   (constante)
    """
    if case not in [1, 2, 3, 4]:
        raise ValueError("case must be 1, 2, 3 or 4")

    f = QuantumCircuit(2)

    if case in [2, 3]:
        f.cx(0, 1)
    if case in [3, 4]:
        f.x(1)

    return f


def dj_query(num_qubits: int) -> QuantumCircuit:
    """Oráculo de uma função aleatória que respeita a promessa do Deutsch-Jozsa."""
    qc = QuantumCircuit(num_qubits + 1)

    if np.random.randint(0, 2):
        # Flip output qubit with 50% chance
        qc.x(num_qubits)
    if np.random.randint(0, 2):
        # return constant circuit with 50% chance
        return qc

    # Choose half the possible input strings
    on_states = np.random.choice(
        range(2**num_qubits),  # numbers to sample from
        2**num_qubits // 2,  # number of samples
        replace=False,  # makes sure states are only sampled once
    )

    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc

    for state in on_states:
        qc.barrier()  # Barriers help visualize how the functions are created
        qc = add_cx(qc, f"{state:0b}")
        qc.mcx(list(range(num_qubits)), num_qubits)
        qc = add_cx(qc, f"{state:0b}")

    qc.barrier()

    return qc


def run_algorithm(function: QuantumCircuit) -> str:
    """Deutsch / Deutsch-Jozsa: uma execução decide 'constant' ou 'balanced'."""
    measurement = measure_once(compile_circuit(function))
    if set(measurement) == {"0"}:
        return "constant"
    return "balanced"
