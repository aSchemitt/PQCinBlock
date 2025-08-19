#!/bin/bash

source venv/bin/activate

python main.py --sign \
    ecdsa \
    mldsa \
    --runs 2 \
    --warm-up 2 \
    --levels 3 5
