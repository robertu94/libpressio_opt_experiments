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
 

for dataload in "${dataloads[@]}"
do
  for tolerance in $(seq 60 10 100)
  do

    read -d '' script <<EOF
local cr = metrics['/pressio/sz/composite/size:size:compression_ratio'];
local psnr = metrics['/pressio/sz/composite/error_stat:error_stat:psnr'];
local threshold = $tolerance.0;
local objective = 0;
if psnr ~= nil and psnr < threshold then
  objective = 0;
else
  objective = cr;
end
return "objective", objective
EOF

    read -d '' script2 <<EOF
local cr = metrics['/pressio/composite/size:size:compression_ratio'];
local psnr = metrics['/pressio/composite/error_stat:error_stat:psnr'];
local threshold = $tolerance.0;
local objective = 0;
if psnr ~= nil and psnr < threshold then
  objective = 0;
else
  objective = cr;
end
return "objective", objective
EOF

    echo "$dataload" "tolerance=$tolerance" "libpressio+sz"

mpiexec pressio -Q  -M all \
       $dataload \
       -b "/pressio:opt:compressor=sz" \
       -b "/pressio:opt:search=guess_first" \
       -b "/pressio:opt:search_metrics=composite_search" \
       -b "/pressio/guess_first:guess_first:search=dist_gridsearch" \
       -b "/pressio/guess_first/dist_gridsearch:dist_gridsearch:search=fraz" \
       -b "/pressio/composite:composite:plugins=size" \
       -b "/pressio/composite:composite:plugins=time" \
       -b "/pressio/composite:composite:plugins=error_stat" \
       -b "/pressio/composite:composite:names=size" \
       -b "/pressio/composite:composite:names=time" \
       -b "/pressio/composite:composite:names=error_stat" \
       -o "/pressio/composite:composite:scripts=$script2" \
       -b "/pressio/sz:sz:metric=composite" \
       -b "/pressio/sz/composite:composite:plugins=size" \
       -b "/pressio/sz/composite:composite:plugins=error_stat" \
       -b "/pressio/sz/composite:composite:names=size" \
       -b "/pressio/sz/composite:composite:names=error_stat" \
       -o "/pressio/sz/composite:composite:scripts=$script" \
       -o "/pressio/guess_first/dist_gridsearch/fraz:opt:local_rel_tolerance=10" \
       -o "/pressio/guess_first:opt:target=60" \
       -o "/pressio/guess_first/dist_gridsearch:dist_gridsearch:num_bins=12" \
       -o "/pressio/guess_first/dist_gridsearch:dist_gridsearch:overlap_percentage=.1" \
       -o "/pressio/guess_first/dist_gridsearch:opt:lower_bound=1e-12" \
       -o "/pressio/guess_first/dist_gridsearch:opt:upper_bound=10" \
       -o "/pressio/guess_first:opt:global_rel_tolerance=.1" \
       -o "/pressio/sz:sz:error_bound_mode_str=abs" \
       -o "/pressio:opt:objective_mode_name=max" \
       -o "/pressio:opt:inputs=/pressio/sz:sz:abs_err_bound" \
       -o "/pressio:opt:output=/pressio/sz/composite:composite:objective" \
       -o "/pressio:opt:output=/pressio/sz/composite/error_stat:error_stat:psnr" \
       -o "/pressio:opt:output=/pressio/sz/composite/size:size:compression_ratio" \
       opt
 
    read -d '' script3 <<EOF
local cr = metrics['/pressio/mgard/composite/size:size:compression_ratio'];
local psnr = metrics['/pressio/mgard/composite/error_stat:error_stat:psnr'];
local threshold = $tolerance.0;
local objective = 0;
if psnr ~= nil and psnr < threshold then
  objective = 0;
else
  objective = cr;
end
return "objective", objective
EOF

    echo "$dataload" "tolerance=$tolerance" "libpressio+mgard"

mpiexec pressio -Q -M all \
      $dataload \
      -b "/pressio:opt:compressor=mgard" \
      -b "/pressio:opt:search=guess_first" \
      -b "/pressio:opt:search_metrics=composite_search" \
      -b "/pressio/guess_first:guess_first:search=dist_gridsearch" \
      -b "/pressio/guess_first/dist_gridsearch:dist_gridsearch:search=fraz" \
      -b "/pressio/composite:composite:plugins=size" \
      -b "/pressio/composite:composite:plugins=time" \
      -b "/pressio/composite:composite:plugins=error_stat" \
      -b "/pressio/composite:composite:names=size" \
      -b "/pressio/composite:composite:names=time" \
      -b "/pressio/composite:composite:names=error_stat" \
      -b "/pressio/mgard:mgard:metric=composite" \
      -b "/pressio/mgard/composite:composite:plugins=size" \
      -b "/pressio/mgard/composite:composite:plugins=error_stat" \
      -b "/pressio/mgard/composite:composite:names=size" \
      -b "/pressio/mgard/composite:composite:names=error_stat" \
      -o "/pressio/composite:composite:scripts=$script2" \
      -o "/pressio/mgard/composite:composite:scripts=$script3" \
      -o "/pressio/guess_first/dist_gridsearch/fraz:opt:local_rel_tolerance=10" \
      -o "/pressio/guess_first:opt:target=60" \
      -o "/pressio/guess_first/dist_gridsearch:dist_gridsearch:num_bins=3" \
      -o "/pressio/guess_first/dist_gridsearch:dist_gridsearch:num_bins=4" \
      -o "/pressio/guess_first/dist_gridsearch:dist_gridsearch:overlap_percentage=.1" \
      -o "/pressio/guess_first/dist_gridsearch:dist_gridsearch:overlap_percentage=.1" \
      -o "/pressio/guess_first/dist_gridsearch:opt:lower_bound=.3" \
      -o "/pressio/guess_first/dist_gridsearch:opt:lower_bound=1e-8" \
      -o "/pressio/guess_first/dist_gridsearch:opt:upper_bound=2" \
      -o "/pressio/guess_first/dist_gridsearch:opt:upper_bound=10" \
      -o "/pressio/guess_first:opt:global_rel_tolerance=.1" \
      -o "/pressio/guess_first:opt:prediction=1.0" \
      -o "/pressio/guess_first:opt:prediction=1e-6" \
      -o "/pressio:opt:objective_mode_name=max" \
      -o "/pressio:opt:inputs=/pressio/mgard:mgard:s" \
      -o "/pressio:opt:inputs=/pressio/mgard:mgard:tolerance" \
      -o "/pressio:opt:output=/pressio/mgard/composite:composite:objective" \
      -o "/pressio:opt:output=/pressio/mgard/composite/error_stat:error_stat:psnr" \
      -o "/pressio:opt:output=/pressio/mgard/composite/size:size:compression_ratio" \
      opt

    echo "$dataload" "tolerance=$tolerance" "sz+psnr"

    read -d '' szobjective <<EOF
local cr = metrics['size:compression_ratio'];
local psnr = metrics['error_stat:psnr'];
local threshold = $tolerance.0;
local objective = 0;
if psnr ~= nil and psnr < threshold then
  objective = 0;
else
  objective = cr;
end
return "objective", objective
EOF

    pressio -M all -m time -m size -m error_stat \
      $dataload \
      -o composite:scripts="$szobjective" \
      -o sz:error_bound_mode_str=psnr \
      -o sz:psnr_err_bound=$tolerance \
      sz

  done
done
