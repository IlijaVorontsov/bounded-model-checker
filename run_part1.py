from pysat.formula import CNF
from subprocess import run
from argparse import ArgumentParser
from AigerCircuit import AigerCircuit


class BoundedModelChecker:
    def __init__(self, circuit: AigerCircuit):
        self.circuit = circuit

        self.cnf = CNF()
        self.cnf.append([1]) # Aiger x_0 is always true (DIMACS literal 1)
        
        for latch in self.circuit.latches:
            self.cnf.append([-latch[0]]) # latch output initialized to 0

    def add_transition_system(self, depth: int):
        if depth > 0:
            for latch in self.circuit.latches:
                # (o^depth+1 <-> i^depth) == (-o^depth+1 | i^depth) & (o^depth+1 | -i^depth)
                self.cnf.append([-self.literal_at(latch[0], depth), self.literal_at(latch[1], depth-1)]) 
                self.cnf.append([self.literal_at(latch[0], depth), -self.literal_at(latch[1], depth-1)])

        for and_gate in self.circuit.and_gates:
            # (o <-> (a1 & a2)) == (-o | a1) & (-o | a2) & (o | -a1 | -a2)
            self.cnf.append([-self.literal_at(and_gate[0], depth), self.literal_at(and_gate[1], depth)])  
            self.cnf.append([-self.literal_at(and_gate[0], depth), self.literal_at(and_gate[2], depth)])
            self.cnf.append([self.literal_at(and_gate[0], depth), -self.literal_at(and_gate[1], depth), -self.literal_at(and_gate[2], depth)])   

    def run_solver(self) -> bool:
        returncode = run("MiniSat-p_v1.14/minisat input.txt > /dev/null", shell=True).returncode
        assert returncode in [10, 20]
        return returncode == 10 # 10 if sat, 20 if unsat

    def check_model_at(self, depth: int) -> bool:
        self.add_transition_system(depth)

        tmp_cnf = self.cnf.copy() # copy to incrementally add clauses only output clause changes rest can be appended
        # o^0 | o^1 | ... | o^depth
        tmp_cnf.append([self.literal_at(self.circuit.output, i) for i in range(depth+1)])     
        
        tmp_cnf.to_file("input.txt")
        return not self.run_solver()

    # returns True if the model is correct, False otherwise
    def check_model(self, depth) -> bool:        
        for i in range(depth + 1):
            if not self.check_model_at(i):
                return False
        return True

    def literal_at(self, literal: int, depth: int) -> int:
        if literal in [-1, 1]: # constant case
            return literal
        if literal < -1:
            return literal - depth*self.circuit.maxvar
        elif literal > 1:
            return literal + depth*self.circuit.maxvar
    
    def __del__(self):
        run("rm input.txt", shell=True)
        

if __name__ == '__main__':
    parser = ArgumentParser(description='Run a bounded model checker on the given AIGER file')
    parser.add_argument('filename', type=str, help='Filename of the AIGER file')
    parser.add_argument('k', type=int, help='Number of steps to check for the safety property')

    args = parser.parse_args()

    circuit = AigerCircuit(args.filename)
    if BoundedModelChecker(circuit).check_model(args.k):
        print("OK")
    else:
        print("FAIL")
