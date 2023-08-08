from Clause import Clause
from Formula import CNF_Formula

class Interpolant:
    def __init__(self, prooffile: str, b: list[list[int]]) -> None:
        clauses = list()
        for clause in b:
            clauses.append(Clause(clause))

        self.b = CNF_Formula(clauses)
        
        self.atoms_b = set()
        for clause in self.b.clauses:
            for literal in clause.literals:
                self.atoms_b.add(abs(literal))
        
        # Preprocess proof
        with open(prooffile, "r") as proof_file:
            self.proof = proof_file.readlines()

        while not self.proof[0].startswith("0:"):
            self.proof.pop(0)

        # removes lines from bottom until "number:"
        while not self.proof[-1].split()[0][:-1].isdigit():
            self.proof.pop(-1)
        
        self.labels = [0] * (len(self.proof))
    
    def clauses(self) -> CNF_Formula:
        return self.getLabel(-1)
        
    def getLabel(self, number: int) -> list[list[int]]:
        line = self.proof[number]
        parts = line.split()
        number, type = int(parts[0][:-1]), parts[1]
        if self.labels[number] != 0: # already computed
            return self.labels[number]
        match type:
            case "ROOT":
                clause = Clause([int(lit) for lit in parts[2:]])
                if self.b.has_clause(clause):
                    self.labels[number] = CNF_Formula([Clause([1])])
                    return self.labels[number]
                else:
                    clause.keep(self.atoms_b)
                    self.labels[number] = CNF_Formula([clause])

                    return self.labels[number]
            case "CHAIN":
                parents, resolved_literals = self.getChainParentsAndResolvants(line)
                label = self.getLabel(parents[0])
                for i in range(len(parents) - 1):
                    if self.resolvedLiteralNotInB(resolved_literals[i]): # OR over clauses
                        label = label * self.getLabel(parents[i+1]) # Cross product
                    else:  # AND over clauses
                        label = label + self.getLabel(parents[i+1]) # Union
                self.labels[number] = label
                return self.labels[number]
            

    def resolvedLiteralNotInB(self, resolved_literal):
        return resolved_literal not in self.atoms_b

    @staticmethod
    def getChainParentsAndResolvants(step_string):
        parts = step_string.split()
        assert parts[1] == "CHAIN"

        resolved_literals = list()
        parents = list()

        for i in range(2, len(parts)):
            if parts[i] == "=>":
                break
            elif parts[i][0] == "[":
                resolved_literals.append(int(parts[i][1:-1])) # remove brackets
            else:
                parents.append(int(parts[i]))

        return parents, resolved_literals
    
   

if __name__ == "__main__":
    # Test case taken from the book with a = 2, b = 3, ...
    interpolant = Interpolant("tests/interpolant_proof.txt", [[3, -5]])
    clauses = interpolant.clauses()
    if clauses.to_list() != [[-3], [5]]:
        print("Interpolant [FAIL]")
        print(f'Expected: [[-3], [5]]')
        print(f'Actual: {clauses.clauses}')
    else:
        print("Interpolant [PASS]")
