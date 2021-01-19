
# run_avg.sh 

- mgard+libpressio crashed, so was excluded
- computes the weighted average timing results used for MGARD-QOI results

# run_early.sh

- compares early termination to normal termination for SZ and MGARD
- produced mgard-2020-10-16-target5.csv and early-2020-10-16.csv

# run_mgard_qoi.sh and run_mgard_qoi_impl.sh

- the non-impl version spread several PSNRs out using GNU parallel
- erroneous script to use MGARD with PSNR

# run_mgard.sh

- compares mgard+libpressio, sz+libpressio, and sz+psnr modes

# run_threads.sh

- runs a different number of threads for FRAZ


# run_zfp.sh

- runs zfp with different numbers of threads

# extract_slice.py

- extracts a slice from a data file for faster experiments

# parse_mgard.py

- parses the results from run_early, and run_mgard scripts


# parse_zfp.py

- parses the results from the run_zfp script

# parse_evaluation.py

- parses the results from the full scale climate evaluation

# plot_evaluation.py

- plots the full scale climate evaluation

# plot_mgard.py

- plots figure 6

# plot_speedups.py

- plots the early termination speedup

# plot_thread_speedup.py

- plots the speedup from threading the search

# plot_zfp.py

- plots the speedup from using threaded ZFP

# run_climate.py

- runs the search for the climate metrics

# run_evaluation.py

- runs the trial based early termination metrics
