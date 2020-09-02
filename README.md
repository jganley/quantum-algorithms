## Quantum Algorithms

These Python classes implement a Grover's algorithm solver using two different quantum programming libraries, PyQuil and Qiskit. The GroverSolver
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
