#!/usr/bin/env bash


qsub run_climate.sh
qsub run_evaluation.sh
qsub -q dicelab run_mgard_qoi.sh
qsub run_mgard.sh
