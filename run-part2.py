from run_part1 import *


class BMC_with_Interpolants(BoundedModelChecker):
    def __init__(self, circuit: AigerCircuit):
        self.circuit = circuit

    def run_minisat(self) -> bool:
        if run("~/bin/minisat input.txt -c > proof.txt", shell=True).returncode == 20: # 10 if sat, 20 if unsat
            run("sed -i 1,16d proof.txt", shell=True) #remove first 16 lines
            return True
        else:
            return False

    def check_depth(self, depth: int) -> bool:
        self.cnf = CNF()
        self.cnf.add_clauses([1]) # Aiger x_0 is always true (DIMACS variable 1)
        if depth == 0:
            return self.add_initial_state()
        
        self.add_interpolant
        self.add_transition_system(depth)
        self.add_output(depth)
        
        
    
    def check_model(self):
        depth = 0
        while self.check_depth(depth):
            if self.check_depth(depth):
                return depth
            else:
                depth += 1

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
