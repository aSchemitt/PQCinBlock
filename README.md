# BlockSignPQC

[Demo Video](https://youtu.be/CNKmvOyZqm0)

**BlockSignPQC** is a modular and extensible benchmark for evaluating post-quantum digital signature (PQC) algorithms in blockchain environments.
It enables direct cryptographic performance measurements and realistic blockchain network simulations through integration with the BlockSim simulator.

## Table of Contents

- [Objectives](#objectives)
- [Tool Structure](#tool-structure)
- [Directory Structure](#directory-structure)
- [Requirements](#requirements)
- [Argument List](#argument-list)
- [Execution](#execution)
- [Adding New Algorithms](#adding-new-algorithms)
- [Evaluating the Impact of Algorithms on Blockchain Simulation](#evaluating-the-impact-of-algorithms-on-blockchain-simulation)
- [License](#license)


## Objectives

- Compare classical algorithms (e.g., ECDSA) and post-quantum algorithms (e.g., Dilithium, Falcon, SPHINCS+).
- Allow continuous and modular integration of new algorithms.
- Simulate the systemic impact of algorithms in blockchain networks.

## Tool Structure

The tool consists of three main modules, each responsible for a specific part of the evaluation process.

1. **`sign_python`**: Executes algorithms and measures signing, verification, and key generation times.
2. **`blocksim`**: Simulates blockchain networks using the collected timing data.
3. **`visualization`**: Generates charts from the data of the previous two modules.

### Directory Structure
```bash
BlockSignPQC/
├── algorithms/           # PQC algorithm implementations (with ALGORITHMS and time_evaluation)
├── BlockSim/             # Blockchain simulator source code (BlockSim)
├── results-paper/        # Complete results used in the paper
├── results/              # Execution results in CSV and charts (not versioned)
├── visualization/        # Chart generation from execution results
├── venv/                 # Python virtual environment (not versioned)
├── graph.py              # Auxiliary chart generation script
├── install.sh            # Main installation script
├── LICENSE               # License file
├── main.py               # Main script orchestrating all steps
├── README.md             # This documentation file
├── requirements.txt      # Required Python dependencies
├── run_experiment.sh     # Runs all experiments described in the paper
├── save.py               # Result saving functions
├── sign_python.py        # Signature algorithms benchmarking module
├── simulator.py          # BlockSim interface and execution with collected data
├── utils.py              # Auxiliary utility functions
```

## Requirements

- [Python 3.11.2](https://www.python.org/downloads/release/python-3112/)
- [liboqs](https://github.com/open-quantum-safe/liboqs)
- [liboqs-python](https://github.com/open-quantum-safe/liboqs-python)

### Installation:

Clone this repository:
```bash
git clone https://github.com/SBSeg25/BlockSignPQC.git
cd BlockSignPQC
```

Make the installation script executable:
```bash
chmod +x install.sh
```

Install the requirements:
```bash
./install.sh
```

>It is recommended to use the same version of `liboqs` and `liboqs-python`. By default, we use version `0.12.0`, defined in the variables at the beginning of [install.sh](./install.sh).

#### Virtual Environment

Activate the virtual environment before running BlockSignPQC.

Activate:
```bash
source venv/bin/activate
```

Deactivate:
```bash
deactivate
```

## Argument List

| Arguments          | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `--sign`           | List of digital signature algorithms to evaluate. Supports multiple values, including classical algorithms (e.g., ECDSA) and post-quantum ones (e.g., Dilithium, Falcon, SPHINCS+). |
| `--runs`           | Number of executions for each algorithm to collect metrics. |
| `--warm-up`        | Number of warm-up runs before the main measurement to stabilize performance.   |
| `--levels`         | Defines the NIST security levels (1 to 5) of the algorithms to be tested. Supports multiple values. |
| `--runs-simulator` | Number of simulation runs in *BlockSim*. |
| `--list-sign`      | Displays all available signature algorithms in the tool. |
| `--help`           | Shows the help message with the description of all available arguments and usage instructions. |


## Execution

Check available arguments with:
```bash
python main.py --help
```

```text
usage: main.py [-h]
               [--sign {sphincs-sha-f,mldsa,cross-rsdpg-balanced,cross-rsdp-fast,ecdsa,cross-rsdpg-fast,sphincs-sha-s,falcon,falcon-padded,cross-rsdp-balanced,mayo,sphincs-shake-f,cross-rsdp-small,cross-rsdpg-small,dilithium,sphincs-shake-s} [{sphincs-sha-f,mldsa,cross-rsdpg-balanced,cross-rsdp-fast,ecdsa,cross-rsdpg-fast,sphincs-sha-s,falcon,falcon-padded,cross-rsdp-balanced,mayo,sphincs-shake-f,cross-rsdp-small,cross-rsdpg-small,dilithium,sphincs-shake-s} ...]]
               [--levels {1,2,3,4,5} [{1,2,3,4,5} ...]] [--runs RUNS] [--warm-up WARM_UP] [--list-sign] [--runs-simulator RUNS_SIMULATOR]

BlockSignPQC

options:
  -h, --help            show this help message and exit
  --sign {sphincs-sha-f,mldsa,cross-rsdpg-balanced,cross-rsdp-fast,ecdsa,cross-rsdpg-fast,sphincs-sha-s,falcon,falcon-padded,cross-rsdp-balanced,mayo,sphincs-shake-f,cross-rsdp-small,cross-rsdpg-small,dilithium,sphincs-shake-s} [{sphincs-sha-f,mldsa,cross-rsdpg-balanced,cross-rsdp-fast,ecdsa,cross-rsdpg-fast,sphincs-sha-s,falcon,falcon-padded,cross-rsdp-balanced,mayo,sphincs-shake-f,cross-rsdp-small,cross-rsdpg-small,dilithium,sphincs-shake-s} ...]
                        Input list of digital signature algorithms (default: None)
  --levels {1,2,3,4,5} [{1,2,3,4,5} ...], -l {1,2,3,4,5} [{1,2,3,4,5} ...]
                        NIST levels (default: range(1, 6))
  --runs RUNS, -r RUNS  Number of executions (default: 1)
  --warm-up WARM_UP, -wp WARM_UP
                        Number of warm-up executions (default: 0)
  --list-sign           List of variants digital signature algorithms (default: False)
  --runs-simulator RUNS_SIMULATOR
                        Number of simulator runs (default: 0)
```

### Listing Algorithms and Variants

Show all available digital signature algorithms:
```bash
python main.py --list-sign
```

Filter by specific NIST security levels:
```bash
python main.py --list-sign --levels <nist_levels>
```

**Example:**
```bash
python main.py --list-sign --levels 1 3 5
```

### Running Algorithm Benchmarks

Run performance tests (sign, verify) for desired algorithms:
```bash
python main.py --sign <algorithms> --runs <n> --warm-up <n> --levels <nist_levels>
```

**Example**
```bash
python main.py --sign ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --runs 5 --warm-up 5 --levels 3 5
```

### Running Blockchain Simulations

Use `--runs-simulator` to define how many times each variant will be executed in the simulator:
```bash
python main.py --sign ecdsa mldsa falcon sphincs-sha-s sphincs-shake-f --runs 5 --warm-up 5 --levels 1 3 5 --runs-simulator 5
```

## Adding New Algorithms

To add a new algorithm, create a `.py` file in `algorithms/` with the following structure:

```python
import pandas as pd

ALGORITHMS = {
    # The levels (1 to 5) can be defined according to the algorithm’s availability.
    # It is not mandatory to fill in all levels.
    "algorithm_name": {
        <level_1>: "variant_name",
        <level_2>: "variant_name",
        <level_3>: "variant_name",
        <level_4>: "variant_name",
        <level_5>: "variant_name",
    }, ...
}

def time_evaluation(variant: str, runs: int):
    
    # Implement the benchmark logic for the given algorithm variant.
    # This function should return a DataFrame with 'sign' and 'verify' execution times.

    return pd.DataFrame({
        'variant': [variant] * runs,
        'sign': time_sign,
        'verify': time_verify
    })
```

## Reproducing the Experiments Described in the Paper

This section describes the step-by-step process for reproducing the experiments in the paper. The experiments are automated and organized to allow independent validation of the experimental.


> Complete results used in the paper are available in [`results-paper`](./results-paper/)


### Execution Environment

The experiments were performed in two hardware configurations:

- **Machine M1**
  - AMD Ryzen 7 5800X
  - Ubuntu 22.04.5 LTS
  - 64 GB RAM

- **Machine M2**
  - Intel(R) Core(TM) i7-9700
  - Debian GNU/Linux 12
  - 16 GB RAM


### Installation and Setup

1. Clone this repository:
```bash
git clone https://github.com/SBSeg25/BlockSignPQC.git
cd BlockSignPQC
```

2. Grant execution permission to the script:
```bash
chmod +x install.sh
```

3. Install the requirements:
```bash
./install.sh
```

4. Activate the virtual environment:
```bash
source venv/bin/activate
```

### Evaluating the Impact of Algorithms on Blockchain Simulation

**Goal:** Simulate the impact of algorithms on block verification times in a blockchain network, using BlockSim, for NIST security levels 1, 3, and 5.

**Command:**
```bash
python main.py --sign \
    ecdsa \
    mldsa \
    sphincs-sha-s \
    sphincs-sha-f \
    sphincs-shake-s \
    sphincs-shake-f \
    falcon \
    mayo \
    cross-rsdp-small \
    cross-rsdpg-small \
    cross-rsdp-balanced \
    cross-rsdpg-balanced \
    cross-rsdp-fast \
    cross-rsdpg-fast \
    --runs 10000 \
    --warm-up 1000 \
    --levels 1 3 5 \
    --runs-simulator 1000
```

**Setup:**

- Flags used: `--sign`, `--runs`, `--warm-up`, `--levels`, `--runs-simulator`.
- Estimated runtime: 10–12 hours depending on the machine used (M1 or M2).
- Results: CSV files and charts in `./results/`.

## License

This project is distributed under the MIT license. See [`LICENSE`](./LICENSE) for details.
