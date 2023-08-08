# bounded-model-checker
Project for exercise part of computer aided verification course.

## Benchmarks
Benchmarks have to run with depth k=30 and within 10 minutes.
`aigbmc` was used to determine the correct output for the benchmarks.

* `benchmarks/nusmv.tcas-t^1.B.aig` is violated at k=11.
* `benchmarks/texas.ifetch1^5.E.aig` at k=20.
* `benchmarks/texas.PI_main^02.E.aig` at k=3.
* `benchmarks/texas.two_proc^1.E.aig` at k=14.
* `benchmarks/vis.eisenberg.E.aig` at k=20.

Install `aigbmc` by running the install-script `./install-aigbmc.sh`
Then run the benchmarks with `./aigbmc -m <benchmark> <k>`.
The option `-m` is important since the outputs are used as bad state detectors.

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

