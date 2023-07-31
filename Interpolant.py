from typing import List

def calculateInterpolant(self, b) -> List[int]:
    clause_b = b
    atoms_b = [abs(literal) for literal in b]
    labels = list()
    proof_file = open("proof.txt", "r")
    while True:
        step_string = proof_file.readline()
        parts = step_string.split()
        match parts[1]:
            case "ROOT":
                clause = [int(lit) for lit in parts[2:]]
                if clause == clause_b: # clause is in B
                    labels.append([[-1]])
                else:
                    labels.append([dropLiteralsNotInB(clause, atoms_b)])
            case "CHAIN":
                parents, resolved_literals = getChainParentsAndResolvants(step_string)
                labels.append(labels[parents[0]])
                for i in range(len(parents) - 1):
                    if self.resolvedVarNotInB(resolved_literals[i]): # OR over clauses
                        label = list()
                        # transform to CNF
                        for clause_p1 in label[-1]:
                            for clause_p2 in label[parents[i+1]]:
                                label.append(clause_p1 + clause_p2) # cross product of clauses (simplification done more efficient by sat solver)
                        labels[-1] = label
                    else:  # AND over clauses
                        labels[-1] = labels[-1] + labels[parents[i+1]] # concat lists 
        if not step_string:
            proof_file.close()
            return labels[-1]
    

def dropLiteralsNotInB(clause, atoms_b):
    return [literal for literal in clause if abs(literal) in atoms_b]

def resolvedLiteralNotInB(resolved_literal, atoms_b):
    return abs(resolved_literal) not in atoms_b

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