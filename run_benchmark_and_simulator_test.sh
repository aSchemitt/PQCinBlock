#!/bin/bash

python main.py --sign \
    ecdsa \
    mldsa \
    --runs 2 \
    --warm-up 2 \
    --levels 3 5 \
    --model 1 2 \
    --runs-simulator 2

