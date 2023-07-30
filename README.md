# bounded-model-checker
Project for exercise part of computer aided verification course.

## Benchmarks
Benchmarks have to run with depth k=30 and within 10 minutes.

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

## TODO:
- [x] Implement bounded model checker
- [ ] Check what output the benchmarks should have
