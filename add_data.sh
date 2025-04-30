#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Optional: activate your virtual environment
# source /path/to/venv/bin/activate

# Run Python modules in order
python -m scripts.db_fillers.0_add_instances
python -m scripts.db_fillers.1_update_degeneracy_col
python -m scripts.db_fillers.2_update_reduced_gs_hd
python -m scripts.db_fillers.3_update_overlap_dist
python -m scripts.db_fillers.4_update_post_anneal_gs_probs
python -m scripts.db_fillers.5_update_post_anneal_overlap
python -m scripts.db_fillers.7_update_qfi
python -m scripts.db_fillers.9_full_gs_mq