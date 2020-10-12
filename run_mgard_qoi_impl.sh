#!/usr/bin/env bash

tolerance="$1"
dataload="$2"
filename=$(echo $dataload | cut -f 2 -d' ' | cut -d/ -f 3)

read -d '' scriptmgard <<EOF
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

echo "$dataload" "tolerance=$tolerance" "mgard-qoi"
pressio \
$dataload \
-W /tmp/$filename.tol$tolerance.dec \
-m error_stat -m time -m size -M all \
-o mgard:s=1 \
-o mgard:tolerance=$tolerance \
-o mgard:qoi_use_metric=1 \
-o mgard:qoi_metric_name="error_stat:psnr" \
-o "composite:scripts=$scriptmgard" \
mgard

