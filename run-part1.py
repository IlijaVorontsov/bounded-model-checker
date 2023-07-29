import argparse
from pysat.solvers import Minisat22
from AigerCircuit import AigerCircuit

# Returns 
def check_model(circuit: AigerCircuit, depth: int) -> bool:
        solver = Minisat22()
        solver.add_clause([1]) # Aiger x_0 is always true

        for latch in circuit.latches:
            solver.add_clause([-latch[0]]) # latch output initialized to 0
            for i in range(depth):
                solver.add_clause([-variable_at(latch[0], i+1, circuit.maxvar), variable_at(latch[1], i, circuit.maxvar)])
                solver.add_clause([variable_at(latch[0], i+1, circuit.maxvar), -variable_at(latch[1], i, circuit.maxvar)])
        
        # SAT if there exists input sequence such that output is true. OR over all states.
        solver.add_clause([variable_at(circuit.output, i, circuit.maxvar) for i in range(depth+1)])

        for and_gate in circuit.ands:
            for i in range(depth+1):
                solver.add_clause([variable_at(and_gate[0], i, circuit.maxvar), -variable_at(and_gate[1], i, circuit.maxvar)])
                solver.add_clause([variable_at(and_gate[0], i, circuit.maxvar), -variable_at(and_gate[2], i, circuit.maxvar)])
                solver.add_clause([-variable_at(and_gate[0], i, circuit.maxvar), variable_at(and_gate[1], i, circuit.maxvar), variable_at(and_gate[2], i, circuit.maxvar)])
  
        return solver.solve()

def variable_at(variable: int, time: int, maxvar) -> int:
    if variable in [-1, 1]: # constant case
        return variable
    if variable < -1:
        return variable - time*maxvar
    elif variable > 1:
        return variable + time*maxvar
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a bounded model checker on the given AIGER file')
    parser.add_argument('filename', type=str, help='Filename of the AIGER file')
    parser.add_argument('k', type=int, help='Number of steps to check for the safety property')

    args = parser.parse_args()

    circuit = AigerCircuit(args.filename)
    for i in range(args.k+1):
        if check_model(circuit, i): # returns true if a sequence of inputs can be found for the output to be 1
            print("FAIL")
            exit()
    print("OK")
    