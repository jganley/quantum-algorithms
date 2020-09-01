import numpy as np
import math

from pyquil import Program, get_qc
from pyquil.quil import DefGate
from pyquil.gates import *


'''

---------- GROVER'S ALGORITHM SOLVER ---------

This Python class implements a Grover's algorithm solver. The GroverSolver
object is instantiated with two parameters:

    num_qubits : the number of qubits that the circuit needs to have

    f : a reference to the function which maps inputs to 0 if they are "bad"
        values and maps inputs to 1 if they are "awesome" values

The GroverSolver class then builds a circuit that is capable of finding the
input which the function f maps to 1. This is accomplished in 3 steps.

    1. The private method __instantiate_qubits is called. This method creates
       the qubits that later functions will use.

    2. The private method __compute_matrices is called. This method creates the
       three custom matrices that will be needed in the quantum circuit. The
       first is the Z_f matrix. This matrix will flip the amplitude for the
       answer vector. The second matrix is the Z_0 matrix. This matrix
       will flip the amplitude for the 0^n vector. The last matrix is the
       "ne-gate" matrix. This matrix flips the amplitude for every vector.

    3. The private method __build_grover_circuit is called. This method
       compiles all the necessary quantum gates to make a circuit that
       implements Grover's algorithm. This circuit contains Hadamard gates as
       well as the gates defined in step 2.

Once the object is initialized, the users can simply call the method to run the
circuit. This method has one parameters and a return value:

    trials : the number of times to execute the circuit

    return : the result of the trials formatted as a dictionary where each
             qubit index maps to an array which contains the measurement of
             that qubit for each trial

'''


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
