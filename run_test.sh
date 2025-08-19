#!/bin/bash

#source venv/bin/activate

python main.py --sign \
    ecdsa \
    mldsa \
    --levels 3 5 \
    --runs 2 \
    --warm-up 3 \
    --runs-simulator 4