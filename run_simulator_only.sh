#!/bin/bash

# Check if a CSV path was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_csv>"
    exit 1
fi

CSV_FILE="$1"

# Activate the virtual environment
source venv/bin/activate

# Loop over models (currently 1 and 2, but you can extend to 0 1 2 3 if needed)
for MODEL in 1 2; do
    echo ">>> Running with --model $MODEL"
    python main.py --sign \
        ecdsa \
        mldsa \
        dilithium \
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
        --levels 1 2 3 5 \
        --input-file "$CSV_FILE" \
        --model "$MODEL" \
        --runs-simulator 1000
done
