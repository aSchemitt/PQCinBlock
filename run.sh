#!/bin/bash

source venv/bin/activate

python main.py --sign \
    ecdsa \
    mldsa \
    dilithium \
    sphincs-sha-s \
    sphincs-sha-f \
    sphincs-shake-s \
    sphincs-shake-f \
    falcon \
    falcon-padded \
    mayo \
    cross-rsdp-small \
    cross-rsdpg-small \
    cross-rsdp-balanced \
    cross-rsdpg-balanced \
    cross-rsdp-fast \
    cross-rsdpg-fast \
    --runs 10000 \
    --warm-up 1000 \
    --levels 1 2 3 4 5 \
    --runs-simulator 1000

