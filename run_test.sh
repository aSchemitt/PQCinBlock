#!/bin/bash

python main.py --sign \
    ecdsa \
    mldsa \
    --levels 3 5 \
    --runs 3 \
    --warm-up 2 \
    --runs-simulator 2 \
    --model 1 2