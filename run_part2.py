from run_part1 import BoundedModelChecker
from argparse import ArgumentParser
from pysat.formula import CNF
from Interpolant import Interpolant
from Formula import CNF_Formula
from Clause import Clause


class UnboundedModelChecker(BoundedModelChecker):
    def check(self):
        depth = 1
        while self.holds_at(depth):
            # print(f'holds at {depth}')
            if self.invariantConverges(depth):
                return True
            depth += 1
        return False
            

    def invariantConverges(self, depth: int):
        self.cnf = CNF()
        b = []
        b.append(self.property[0])

        for i in range(1, depth+1):
            for clause in self.clauses_transision_system_at(i):
                b.append(clause)

        tmp = []
        for init in self.initial_state:
            tmp.append(Clause(init))
        reachable = CNF_Formula(tmp)

        check_index = 1
        while True:
            check_index += 1
            interpolant = Interpolant("proof.txt", b).clauses().to_list()
            
            interpolant = CNF_Formula(self.substitute_literals(interpolant, 0))

            # print(f'reachable: {interpolant}')
            if interpolant.implies(reachable):
                return True
            
            reachable *= interpolant # Cross Product or OR of clauses
        
            self.cnf = CNF(from_clauses=reachable.to_list())
            self.cnf.append([1])
            self.add_transition_system(depth)
            self.add_property(depth)
            if self.is_sat(): # abort
                return False
    

    def substitute_literals(self, clauses: list[list[int]], depth: int) -> list[list[int]]:
        result = []
        for clause in clauses:
            result.append([])
            for literal in clause:
                result[-1].append(self.literal_at(literal, depth))
        return result

    

if __name__ == '__main__':
    parser = ArgumentParser(description='Run a bounded model checker on the given AIGER file')
    parser.add_argument('filename', type=str, help='Filename of the AIGER file')

    args = parser.parse_args()

    if UnboundedModelChecker(args.filename).check():
        print("OK")
    else:
        print("FAIL")
