# Fair Sampling Research Repository

This is my code for the physics research I am doing Professor Chris Herdman from Middlebury College.

We are exploring quantum annealing on a Ising model spin glass, specifically examing the entanglement structure and "macroscropic quantumness" as it relates to computational hardness and the overall efficacy of quantum adiabatic computation.

# Specs

Uses a SQLite database with Alembic (stored locally in `database/fair_sampling.db`)

Python notebooks used for exploration of ideas in `exploration_notebooks`

More polished scripts to generate data (the results of work from `exploration_notebooks`) in `scripts`

`tfim_sk_infd` is written like a package with useful functionalities.

`data_service.py` facilitates talking to the db and also storing json files locally if needed
