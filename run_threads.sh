#!/usr/bin/env bash
#first extract slices
echo "done preparing"


dataloads=(
"-i ${HOME}/git/datasets/hurricane/100x500x500/CLOUDf48.bin.f32 -t float -d 100 -d 500 -d 500"
)
 

for dataload in "${dataloads[@]}"
do
  for threads in $(seq 1 3 12)
  do
  for tolerance in $(seq 20 10 60)
  do

    read -d '' script <<EOF
local cr = metrics['/pressio/zfp/composite/size:size:compression_ratio'];
local psnr = metrics['/pressio/zfp/composite/error_stat:error_stat:psnr'];
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

    echo "$dataload" "tolerance=$tolerance" "libpressio+zfp/${threads}"

mpiexec -np 3 pressio -Q  -M all \
       $dataload \
       -b "/pressio:opt:compressor=zfp" \
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
       -b "/pressio/zfp:zfp:metric=composite" \
       -b "/pressio/zfp/composite:composite:plugins=size" \
       -b "/pressio/zfp/composite:composite:plugins=error_stat" \
       -b "/pressio/zfp/composite:composite:names=size" \
       -b "/pressio/zfp/composite:composite:names=error_stat" \
       -o "/pressio/zfp/composite:composite:scripts=$script" \
       -o "/pressio/guess_first/dist_gridsearch/fraz:opt:local_rel_tolerance=10" \
       -o "/pressio/guess_first/dist_gridsearch/fraz:fraz:nthreads=${threads}" \
       -o "/pressio/guess_first:opt:target=60" \
       -o "/pressio/guess_first/dist_gridsearch:dist_gridsearch:num_bins=12" \
       -o "/pressio/guess_first/dist_gridsearch:dist_gridsearch:overlap_percentage=.1" \
       -o "/pressio/guess_first/dist_gridsearch:opt:lower_bound=1e-12" \
       -o "/pressio/guess_first/dist_gridsearch:opt:upper_bound=10" \
       -o "/pressio/guess_first:opt:global_rel_tolerance=.1" \
       -o "/pressio:opt:objective_mode_name=max" \
       -o "/pressio:opt:inputs=/pressio/zfp:zfp:accuracy" \
       -o "/pressio:opt:output=/pressio/zfp/composite:composite:objective" \
       -o "/pressio:opt:output=/pressio/zfp/composite/error_stat:error_stat:psnr" \
       -o "/pressio:opt:output=/pressio/zfp/composite/size:size:compression_ratio" \
       opt
 
  done
done
done
