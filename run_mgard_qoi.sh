#!/usr/bin/env bash
#first extract slices

begins=(0 30 50 80)
ends=(3 33 53 83)
for idx in "${!begins[@]}"
do
  begin=${begins[$idx]}
  end=${ends[$idx]}

  slice_num=$(( ($end - $begin) / 2 + $begin ))
  file=/tmp/CLOUD_slice-${slice_num}.f32

  if [[ ! -e "/tmp/CLOUD_slice-${slice_num}.f32" ]]; then
    echo "preparing $file"
    ./extract_slice.py \
      --api 5 \
      --input ~/git/datasets/hurricane/100x500x500/CLOUDf48.bin.f32 \
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
"-i /tmp/CLOUD_slice-1.f32 -t float -d 3 -d 500 -d 500"
"-i /tmp/CLOUD_slice-31.f32 -t float -d 500 -d 500 -d 3"
"-i /tmp/CLOUD_slice-51.f32 -t float -d 500 -d 500 -d 3"
"-i /tmp/CLOUD_slice-81.f32 -t float -d 500 -d 500 -d 3"
)
 

parallel -k ./run_mgard_qoi_impl.sh "{1}" "{2}" ::: $(seq 20 10 60 ) ::: "${dataloads[@]}"
