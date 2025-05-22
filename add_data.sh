#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

N=18
sstart=0
send=5
batch=5

# Optional: activate your virtual environment
# source /path/to/venv/bin/activate

# Run Python modules in order
python -m scripts.db_fillers.0_add_instances "$N" "$sstart" "$send" "$batch"
python -m scripts.db_fillers.1_update_degeneracy_col "$N"
python -m scripts.db_fillers.2_update_reduced_gs_hd "$N"
python -m scripts.db_fillers.3_update_overlap_dist "$N"
python -m scripts.db_fillers.4_update_post_anneal_gs_probs "$N"
python -m scripts.db_fillers.5_update_post_anneal_overlap "$N"
python -m scripts.db_fillers.7_update_qfi "$N"
python -m scripts.db_fillers.9_full_gs_mq "$N"

