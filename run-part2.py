from run_part1 import *
from Interpolant import calculateInterpolant

class BMC_with_Interpolants(BoundedModelChecker):
    def __init__(self, circuit: AigerCircuit):
        self.circuit = circuit

    def run_minisat(self) -> bool:
        if run("MiniSat-p_v1.14/minisat input.txt -c > proof.txt", shell=True).returncode == 20: # 10 if sat, 20 if unsat
            run("sed -i 1,16d proof.txt", shell=True) #remove first 16 lines
            return True
        else:
            return False

    def check_depth(self, depth: int) -> bool:
        self.cnf = CNF()
        self.cnf.add_clauses([1]) # Aiger x_0 is always true (DIMACS variable 1)
        if depth == 0:
            self.add_initial_state()
        else:
            self.last_interpolant = self.interpolant
            self.interpolant = calculateInterpolant(self.b)
            for clause in self.interpolant:
                self.cnf.append(clause)
        self.add_transition_system(depth)
        
        self.b = [self.literal_at(self.circuit.output, i) for i in range(depth+1)]
        self.cnf.append(self.b)

        self.cnf.to_file("input.txt")
        return self.run_minisat()
    
    def check_model(self):
        depth = 0
        while not self.interpolantsConverge():
            if self.check_depth(depth):
                return False
            else:
                depth += 1
        return True

    def interpolantsConverge(self):
        return self.to_base_literals(self.last_interpolant) == self.to_base_literals(self.interpolant)
    
    def to_base_clause(self, clause):
        base_clause = list()
        for literal in clause:
            if literal in [-1, 1]:
                base_clause.append(literal)
            elif literal < -1:
                base_clause.append(-(abs(literal)%self.circuit.maxvar))
            else:
                base_clause.append(abs(literal)%self.circuit.maxvar)
        # remove duplicates and sort
        return list(dict.fromkeys(base_clause)).sort()

    def __del__(self):
        run("rm input.txt proof.txt", shell=True)


if __name__ == '__main__':
    parser = ArgumentParser(description='Run a bounded model checker on the given AIGER file')
    parser.add_argument('filename', type=str, help='Filename of the AIGER file')

    args = parser.parse_args()

    circuit = AigerCircuit(args.filename)
    if BMC_with_Interpolants(circuit).check_model():
        print("OK")
    else:
        print("FAIL")
