#!/bin/bash

python3 make_figs.py
for x in sim_ts/*.svg; do make ${x%%svg}gif; done
make sim_ts.anim.gif
