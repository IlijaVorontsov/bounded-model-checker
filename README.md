# bounded-model-checker
Project for exercise part of computer aided verification course.

## Benchmarks
### Part 1
Benchmarks have to run with depth k=30 and within 10 minutes.
`aigbmc` was used to determine the correct output for the benchmarks.

All **FAIL** at:

* `benchmarks/texas.ifetch1^5.E.aig` k=20.
* `benchmarks/vis.eisenberg.E.aig` k=20.
* `benchmarks/texas.two_proc^1.E.aig` k=14.
* `benchmarks/nusmv.tcas-t^1.B.aig` k=11.
* `benchmarks/texas.PI_main^02.E.aig` k=3.

Install `aigbmc` by running the install-script `./install-aigbmc.sh`
Then run the benchmarks with `./aigbmc -m <benchmark> <k>`.
The option `-m` is important since the outputs are used as bad state detectors.

### Part 2
Results couldn't have been verified. All are **OK** at:

* `benchmarks/nusmv.syncarb5^2.B.aig` k=3 (depth 9)
* `benchmarks/vis.emodel.E.aig` k=1 (depth 4)
* `benchmarks/cmu.gigamax.B.aig` k=2 (depth 5)
* `benchmarks/ken.flash^01.C.aig` k=2 (depth 2)
* `benchmarks/texas.ifetch1^3.E.aig` k=1 (depth 3)

## Usage
```sh
python3 run-part1.py benchmark k
```
```sh
python3 run-part2.py benchmark
```

### Requirements
```
# Tested on Ubuntu 18.04
sudo apt install python3 python3-pip build-essential
pip3 install python-sat
cd MiniSat-p_v1.14/
make
chmod +x minisat
```

