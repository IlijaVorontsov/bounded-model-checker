from pysat.formula import CNF
from subprocess import run
from argparse import ArgumentParser
from AigerCircuit import AigerCircuit


class BoundedModelChecker:
    def __init__(self, aigerfile: str):
        self.circuit = AigerCircuit(aigerfile)
        self.initial_state = [[-latch[0]] for latch in self.circuit.latches]
        self.property = [[self.circuit.output]]

    def add_initial_state(self):
        for clause in self.initial_state:
            self.cnf.append(clause)

    def clauses_transision_system_at(self, depth: int) -> list[list[int]]:
        clauses = []
        for latch in self.circuit.latches:
            # (o^depth+1 <-> i^depth) == (-o^depth+1 | i^depth) & (o^depth+1 | -i^depth)
            clauses.append([-self.literal_at(latch[0], depth+1), self.literal_at(latch[1], depth)]) 
            clauses.append([self.literal_at(latch[0], depth+1), -self.literal_at(latch[1], depth)])

        for and_gate in self.circuit.and_gates:
            # (o <-> (a1 & a2)) == (-o | a1) & (-o | a2) & (o | -a1 | -a2)
            clauses.append([-self.literal_at(and_gate[0], depth), self.literal_at(and_gate[1], depth)])  
            clauses.append([-self.literal_at(and_gate[0], depth), self.literal_at(and_gate[2], depth)])
            clauses.append([self.literal_at(and_gate[0], depth), -self.literal_at(and_gate[1], depth), -self.literal_at(and_gate[2], depth)])
        return clauses
    
    def add_transition_system(self, depth: int):
        for i in range(depth+1):
            for clause in self.clauses_transision_system_at(i):
                self.cnf.append(clause)

    def add_property(self, depth: int):
        # o^0 | o^1 | ... | o^depth
        self.property = [[self.literal_at(self.circuit.output, i) for i in range(depth+1)]]
        for clause in self.property:
            self.cnf.append(clause)

    def is_sat(self) -> bool:
        self.cnf.to_file("input.txt")
        returncode = run("MiniSat-p_v1.14/minisat input.txt -c > proof.txt", shell=True).returncode
        assert returncode in [10, 20]
        return returncode == 10 # 10 if sat, 20 if unsat
    
    def holds_at(self, depth: int) -> bool:
        self.cnf = CNF()
        self.cnf.append([1]) # Aiger x_0 is always true (DIMACS literal 1)

        self.add_initial_state()        
        self.add_transition_system(depth)
        self.add_property(depth)

        return not self.is_sat()

    def check(self, depth: int) -> bool:
        for i in range(depth+1):
            if not self.holds_at(i):
                return False
        return True

    def literal_at(self, literal: int, depth: int) -> int:
        assert literal != 0
        if literal in [1, -1]: # in order to have only one constant clause in the CNF
            return literal
        
        sign = 1 if literal > 0 else -1
        atom = abs(literal)
        atom_at_0 = (atom - 1)%self.circuit.maxvar + 1 # shifting because maxvar = output;
        atom_at_depth = atom_at_0 + depth*self.circuit.maxvar
        return sign*atom_at_depth
        
    def __del__(self):
        pass
        #run("rm input.txt proof.txt", shell=True)
        

if __name__ == '__main__':
    parser = ArgumentParser(description='Run a bounded model checker on the given AIGER file')
    parser.add_argument('filename', type=str, help='Filename of the AIGER file')
    parser.add_argument('k', type=int, help='Number of steps to check for the safety property')

    args = parser.parse_args()

    if BoundedModelChecker(args.filename).check(args.k):
        print("OK")
    else:
        print("FAIL")
