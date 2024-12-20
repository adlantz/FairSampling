# Fair Sampling Research Repository

Uses python 3.11.

Uses a SQLite database with Alembic (stored locally in `database/fair_sampling.db`)

Python notebooks used for exploration of ideas in `exploration_notebooks`

More polished scripts to generate data (the results of work from `exploration_notebooks`) in `scripts`

`tfim_sk_infd` acts like a package with useful functionalities.
Because of python's weirdness around importing, scripts need to be run as modules from the root. I.e
```
python3 -m scripts.toy_models.script
```


`data_service.py` facilitates talking to the db and also storing json files locally if needed
