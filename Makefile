db_fill_0:
	python3 -m scripts.db_fillers.0_add_instances
db_fill_1:
	python3 -m scripts.db_fillers.1_update_degeneracy_col	    
db_fill_2:
	python3 -m scripts.db_fillers.2_update_reduced_gs_hd
db_fill_3:
	python3 -m scripts.db_fillers.3_update_overlap_dist
db_fill_4:
	python3 -m scripts.db_fillers.4_update_post_anneal_gs_probs
db_fill_5:
	python3 -m scripts.db_fillers.5_update_post_anneal_overlap
db_fill_6:
	python3 -m scripts.db_fillers.6_update_disconnectivity
db_fill_7:
	python3 -m scripts.db_fillers.7_update_qfi
db_fill_8:
	python3 -m scripts.db_fillers.8_update_dist

