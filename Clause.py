class Clause:
    def __init__(self, literals:list[int]) -> None:
        self.literals = list()
        literals = sorted(list(set(literals)))
        for literal in literals:
            if literal == 1:
                self.literals = [1]
                break
            elif -literal in literals:
                self.literals = [1]
                break
            else:
                self.literals.append(literal)
        
    def __repr__(self) -> str:
        return self.__str__()
        
    def __str__(self) -> str:
        return str(self.literals)
    
    def __eq__(self, other):
        return self.literals == other.literals
    
    def keep(self, atoms:list[int]):
        new = list()
        for literal in self.literals:
            if abs(literal) in atoms:
                new.append(literal)
    
        self.literals = sorted(new)

    def __len__(self):
        return len(self.literals)
    
    def distribute(self, units:list[int]) -> None:
        new = list()
        for literal in self.literals:
            if literal in units:
                new = [1]
                break
            elif -literal not in units:
                new.append(literal)
        return Clause(new)

    def implies(self, other) -> bool:
        for literal in self.literals:
            if literal not in other.literals:
                return False
        return True


if __name__ == "__main__":
    # testing implies
    c1 = Clause([2, 3])
    c2 = Clause([2, 3, 4])
    assert c1.implies(c2)
    print(c1, "implies", c2, ":", c1.implies(c2))
    assert not c2.implies(c1)
    print(c2, "implies", c1, ":", c2.implies(c1))