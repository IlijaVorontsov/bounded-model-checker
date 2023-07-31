wget https://fmv.jku.at/picosat/picosat-965.tar.gz
tar -xf picosat-965.tar.gz
mv picosat-965 picosat
wget https://fmv.jku.at/lingeling/lingeling-bcj-78ebb86-180517.tar.gz
tar -xf lingeling-bcj-78ebb86-180517.tar.gz
mv lingeling-bcj-78ebb86-180517 lingeling
wget https://fmv.jku.at/aiger/aiger-1.9.9.tar.gz
tar -xf aiger-1.9.9.tar.gz
mv aiger-1.9.9 aiger
rm aiger-1.9.9.tar.gz picosat-965.tar.gz lingeling-bcj-78ebb86-180517.tar.gz
cd picosat
./configure.sh
make
cd ../lingeling
./configure.sh
make
cd ../aiger
./configure.sh
make
mv ./aigbmc ../aigbmc
clean
../aigbmc -h