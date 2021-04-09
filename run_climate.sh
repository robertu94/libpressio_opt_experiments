#!/usr/bin/env bash
#PBS -l select=4:ncpus=40:mem=372gb:mpiprocs=40
#PBS -l walltime=24:00:00
#PBS -M robertu@clemson.edu
#PBS -m abe
#PBS -j oe
#PBS -N run_climate

cd ~/projects/libpressio_opt_experiments/
source ~/git/spack/share/spack/setup-env.sh
spack env activate .

for procs in $(seq 2 10 150)
do
	echo "nprocs=${procs}"
	time ./run_climate.py --search_progress --n_proc ${procs} --target 7.3
done
