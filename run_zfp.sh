#!/usr/bin/env bash

for i in $(seq 1 12)
do
  for replica in $(seq 1 30)
  do
    pressio -i ~/git/datasets/hurricane/100x500x500/CLOUDf48.bin.f32 -d 500 -d 500 -d 100 -t float zfp -m time -M time:compress -o zfp:accuracy=1e-4 -o zfp:omp_threads=$i -o zfp:execution=1 -O zfp:omp_threads
    echo "==="
  done
done 2>&1 | tee /tmp/zfp-threads.log
