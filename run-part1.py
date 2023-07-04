import argparse
from pysat.solvers import Minisat22

# Remaps the AIGER variables to DIMACS variables.
# Since the AIGER x_0 is always true, we map it to DIMACS variable 1.
# All other variables are shifted by 1.
def parse_variable(number_string: str) -> int:
    number = int(number_string)
    if number%2 == 0:
        return number//2 + 1
    else:
        return -number//2 - 1
        

class Checker:
    def __init__(self, filename: str, k: int):
        self.file = open(filename, 'r')
        self.k = k
        self.solver = Minisat22()
        self.solver.add_clause([1]) # Aiger x_0 is always true

        header = self.file.readline().split()
        self.maxvar = int(header[1])
        self.inputs = int(header[2])
        self.latches = int(header[3])
        self.outputs = int(header[4])
        assert self.outputs == 1
        self.ands = int(header[4])

        # skip over inputs
        for _ in range(self.inputs):
            self.file.readline()

        for _ in range(self.latches):
            latch = [parse_variable(number) for number in self.file.readline().split()]
            assert len(latch) == 2
            self.solver.add_clause([-latch[0]]) # latches initialized to 0
            for i in range(self.k):
                self.solver.add_clause([-self.variable_at(latch[0], i+1), self.variable_at(latch[1], i)])
                self.solver.add_clause([self.variable_at(latch[0], i+1), -self.variable_at(latch[1], i)])
        
        output = [parse_variable(number) for number in self.file.readline().split()]
        assert len(output) == 1
        self.output = output[0]

        self.solver.add_clause([self.variable_at(self.output, i) for i in range(self.k+1)])

        for _ in range(self.ands):
            and_gate = [parse_variable(number) for number in self.file.readline().split()]
            assert len(and_gate) == 3
            for i in range(self.k+1):
                self.solver.add_clause([self.variable_at(and_gate[0], i), -self.variable_at(and_gate[1], i)])
                self.solver.add_clause([self.variable_at(and_gate[0], i), -self.variable_at(and_gate[2], i)])
                self.solver.add_clause([-self.variable_at(and_gate[0], i), self.variable_at(and_gate[1], i), self.variable_at(and_gate[2], i)])

    def check(self):
        if self.solver.solve():
            print('OK')
        else:
            print('FAIL')

    def variable_at(self, variable: int, time: int) -> int:
        return variable + time*self.maxvar
    
    def to_latex_variable(self, variable: int) -> str:
        return 'x_{' + str(variable%self.maxvar) + '}^{' + str(variable//self.maxvar) + '}'

    def __del__(self):
        self.file.close()
     
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a bounded model checker on the given AIGER file')
    parser.add_argument('filename', type=str, help='Filename of the AIGER file')
    parser.add_argument('k', type=int, help='Number of steps to check for the safety property')

    args = parser.parse_args()

    checker = Checker(args.filename, args.k)
    checker.check()
