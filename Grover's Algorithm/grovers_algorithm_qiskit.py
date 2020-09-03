import numpy as np
import math

from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info.operators import Operator


'''
##########################################################################
#                                                                        #
#                   GROVER'S ALGORITHM IMPLEMENTATION                    #
#                                                                        #
##########################################################################
'''


class GroverSolver(object):

    def __init__(self, num_qubits, f):
        self.__num_qubits = num_qubits
        self.__f = f
        self.__compute_matrices()
        self.__build_grover_circuit()


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
        p = QuantumCircuit(self.__num_qubits, self.__num_qubits)
        ZF_GATE = Operator(self.__Zf)
        Z0_GATE = Operator(self.__Z0)
        NE_GATE = Operator(self.__Negate)

        # apply first round of Hadamard gates
        for i in range(self.__num_qubits):
            p.h(i)

        # apply Grover as many times as needed
        for i in range(self.__num_iterations()):
            p.append(ZF_GATE, list(range(self.__num_qubits)))
            for i in range(self.__num_qubits):
                p.h(i)
            p.append(Z0_GATE, list(range(self.__num_qubits)))
            for i in range(self.__num_qubits):
                p.h(i)
            p.append(NE_GATE, list(range(self.__num_qubits)))

        # measure the qubits
        p.measure(list(range(self.__num_qubits)), list(range(self.__num_qubits)))

        # save the grover circuit
        self.__grover_circuit = p


    def run(self, trials):
        simulator = Aer.get_backend("qasm_simulator")
        job = execute(self.__grover_circuit, simulator, shots=trials)
        return job.result().get_counts()


'''
##########################################################################
#                                                                        #
#                 CODE FOR RUNNING GROVER'S ALGORITHM                    #
#                                                                        #
##########################################################################
'''


f = lambda x : int(x == '100')
grover_solver = GroverSolver(3, f)

results = grover_solver.run(1000)
print(results)
