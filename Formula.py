from Clause import Clause

class CNF_Formula:
    def __init__(self, clauses) -> None:
        self.clauses = list()
        for clause in clauses:
            if type(clause) == list:
                clause = Clause(clause)
            if clause != Clause([1]):
                self.clauses.append(clause)

        self.distributeUnits()
        self.removeValidClauses()
        self.removeDuplicateClauses()
        self.findContradictions()

    def findContradictions(self):
        for clause in self.clauses:
            if len(clause) == 0:
                self.clauses = [Clause([])]
                return
            if len(clause) == 1:
                literal = clause.literals[0]
                if Clause([-literal]) in self.clauses:
                    self.clauses = [Clause([])]
                    return

    def removeValidClauses(self):
        new_clauses = list()
        for clause in self.clauses:
            if clause != Clause([1]):
                new_clauses.append(clause)
        self.clauses = new_clauses

    def removeDuplicateClauses(self):
        new_clauses = list()
        for clause in self.clauses:
            if clause not in new_clauses:
                new_clauses.append(clause)
        self.clauses = new_clauses
                
    def distributeUnits(self):
        unit_clauses = list()
        new_clauses = list()
        new_units = self.findUnitClauses()
        if len(new_units) == 0:
            return
        while len(new_units) > 0:
            for clause in self.clauses:
                if len(clause) != 1:
                    new_clauses.append(clause.distribute(new_units))

            unit_clauses += new_units
            self.clauses = new_clauses
            new_units = self.findUnitClauses()
            new_clauses = list()

        for unit in unit_clauses:
            self.clauses.append(Clause([unit]))

    def findUnitClauses(self) -> list[int]:
        unit_clauses = list()
        for clause in self.clauses:
            if len(clause) == 1:
                unit_clauses.append(clause.literals[0])
        return unit_clauses
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __str__(self) -> str:
        return str(self.clauses)
    
    def __mul__(self, other):
        clauses = list()
        for clause_1 in self.clauses:
            for clause_2 in other.clauses:
                clauses.append(Clause(clause_1.literals + clause_2.literals))
        return CNF_Formula(clauses)
    
    def __add__(self, other):
        return CNF_Formula(self.clauses + other.clauses)
    
    def has_clause(self, clause:Clause) -> bool:
        return clause in self.clauses
    
    def to_list(self) -> list[Clause]:
        l = list()
        for clause in self.clauses:
            l.append(clause.literals)
        return l
    
    def implies(self, other):
        # For all clauses in other, check if subset of them are in self
        found_implication = False
        for clause in other.clauses:
            for clause_2 in self.clauses:
                if clause_2.implies(clause):
                    found_implication = True
                    break
            if not found_implication:
                return False
            found_implication = False
        return True

if __name__ == "__main__":
    # Tests
    # Contradiction afer distribution
    formula = CNF_Formula([Clause([2]), Clause([-2,3]), Clause([-2,-3]), Clause([5,6])])
    assert formula.to_list() == [[]]
    # Removing valid clauses
    formula = CNF_Formula([Clause([2]), Clause([2,3]), Clause([-2, 3,-3]), Clause([5,6]), Clause([1])])
    print(formula)

    # Implication
    formula = CNF_Formula([Clause([2]), Clause([2,3]), Clause([-2, 3,-3]), Clause([5,6]), Clause([1])])
    formula_2 = CNF_Formula([Clause([2,3]), Clause([5,6]), Clause([1])])
    print(f"{formula} implies {formula_2}")
    assert formula.implies(formula_2)
    assert not formula_2.implies(formula)