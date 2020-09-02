import numpy as np
import math

from pyquil import Program, get_qc
from pyquil.quil import DefGate
from pyquil.gates import *


class GroverSolver(object):

    def __init__(self, num_qubits, f):
        self.__num_qubits = num_qubits
        self.__f = f
        self.__instantiate_qubits()
        self.__compute_matrices()
        self.__build_grover_circuit()


    def __instantiate_qubits(self):
        self.__qubits = list(range(int(self.__num_qubits)))


    def __compute_matrices(self):
        # build Zf matrix based on function f
        Zf_gate = np.identity(2**self.__num_qubits)
        for i in range(2**self.__num_qubits):
            if self.__f(format(i, '0' + str(self.__num_qubits) + 'b')) == 1:
                Zf_gate[i, i] = -1
                break
        self.__Zf = Zf_gate

        # build Z0 matrix where 0th vector is negated
        Z0_gate = np.identity(2**self.__num_qubits)
        Z0_gate[0,0] = -1
        self.__Z0 = Z0_gate

        # build negation gate where all amplitudes are negated
        Ne_gate = np.identity(2**self.__num_qubits)
        for i in range(2**self.__num_qubits):
            Ne_gate[i, i] *= -1
        self.__Negate = Ne_gate


    def __num_iterations(self):
        return math.floor((math.pi / 4) * math.sqrt(2**self.__num_qubits))


    def __build_grover_circuit(self):
        # initialize program and define new gates
        p = Program()
        p.defgate("ZF_GATE", self.__Zf)
        p.defgate("Z0_GATE", self.__Z0)
        p.defgate("NE_GATE", self.__Negate)

        # apply first round of Hadamard gates
        for i in range(self.__num_qubits):
            p += H(i)

        # apply Grover as many times as needed
        for i in range(self.__num_iterations()):
            p.inst(tuple(["ZF_GATE"] + self.__qubits))
            for i in range(self.__num_qubits):
                p += H(i)
            p.inst(tuple(["Z0_GATE"] + self.__qubits))
            for i in range(self.__num_qubits):
                p += H(i)
            p.inst(tuple(["NE_GATE"] + self.__qubits))

        # save the grover circuit
        self.__grover_circuit = p


    def run(self, trials):
        qc = get_qc(f"{self.__num_qubits}q-qvm")
        return qc.run_and_measure(self.__grover_circuit, trials=trials)
