#!/bin/bash

source venv/bin/activate

python main.py --sign \
    ecdsa \
    mldsa \
    falcon \
    falcon-padded \
    mayo \
    sphincs-sha-s \
    sphincs-sha-f \
    sphincs-shake-s \
    sphincs-shake-f \
    cross-rsdp-small \
    cross-rsdpg-small \
    cross-rsdp-balanced \
    cross-rsdpg-balanced \
    cross-rsdp-fast \
    cross-rsdpg-fast \
    --runs 1 \
    --warm-up 1 \
    --levels 1 2 3 5
