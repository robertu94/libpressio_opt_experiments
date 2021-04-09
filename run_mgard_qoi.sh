#!/usr/bin/env bash
#PBS -l select=4:ncpus=40:mem=372gb:mpiprocs=40
#PBS -l walltime=24:00:00
#PBS -M robertu@clemson.edu
#PBS -m abe
#PBS -j oe
#PBS -N run_mgard_qoi
#first extract slices

cd ~/projects/libpressio_opt_experiments/
source ~/git/spack/share/spack/setup-env.sh
spack env activate .

begins=(0 30 50 80)
ends=(3 33 53 83)
for idx in "${!begins[@]}"
do
  begin=${begins[$idx]}
  end=${ends[$idx]}

  slice_num=$(( ($end - $begin) / 2 + $begin ))
  file=$TMPDIR/CLOUD_slice-${slice_num}.f32

  if [[ ! -e "$TMPDIR/CLOUD_slice-${slice_num}.f32" ]]; then
    echo "preparing $file"
    ./extract_slice.py \
      --api 5 \
      --input /zfs/fthpc/common/sdrbench/hurricane/CLOUDf48.bin \
      --type float \
      --dims 100 \
      --dims 500 \
      --dims 500 \
      --external_outfile $file \
      --external_from_slice $begin \
      --external_to_slice $end \
      --external_slice_dim 0 \
      >/dev/null
      

  else 
    echo "skipping $file, exists"
  fi
done

echo "done preparing"


dataloads=(
"-i $TMPDIR/CLOUD_slice-1.f32 -t float -d 3 -d 500 -d 500"
"-i $TMPDIR/CLOUD_slice-31.f32 -t float -d 3 -d 500 -d 500"
"-i $TMPDIR/CLOUD_slice-51.f32 -t float -d 3 -d 500 -d 500"
"-i $TMPDIR/CLOUD_slice-81.f32 -t float -d 3 -d 500 -d 500"
)
 

parallel -k ./run_mgard_qoi_impl.sh "{1}" "{2}" ::: 1e-3 1e-4 1e-5 ::: "${dataloads[@]}"
