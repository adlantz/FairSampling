# Fair Sampling Research Repository

Uses python 3.11.

Results in `data/`, scripts to generate data in `scripts/`.

`tfim_sk_infd` acts like a package with useful funcionalities that are imported by scripts.

Because of python's weirdness around importing, scripts need to be run as modules from the root. I.e
```
python3 -m scripts.toy_models.script
```
