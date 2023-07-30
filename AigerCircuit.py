class AigerCircuit:
    def __init__(self, filename: str):
        with open(filename, "r") as aigerfile:
            header = aigerfile.readline().split()
            self.maxvar = int(header[1])

            # skip over inputs
            for _ in range(int(header[2])):
                aigerfile.readline()

            self.latches = []
            for _ in range(int(header[3])):
                latch = parse_line(aigerfile)
                assert len(latch) == 2
                self.latches.append(latch)

            assert int(header[4]) == 1 # Bad state detector by assignment (only one output state)
            output = parse_line(aigerfile)
            assert len(output) == 1
            self.output = output[0]

            self.and_gates = []
            for _ in range(int(header[5])):
                and_gate = parse_line(aigerfile)
                assert len(and_gate) == 3
                self.and_gates.append(and_gate)
                
    
def parse_line(file):
    return [parse_variable(number) for number in file.readline().split()]

# Remaps the AIGER variables to DIMACS variables.
# Since the AIGER x_0 is always true, we map it to DIMACS variable 1.
# All other variables are shifted by 1.
def parse_variable(number_string: str) -> int:
    number = int(number_string)
    if number%2 == 0:
        return number//2 + 1
    else:
        return -number//2 - 1
