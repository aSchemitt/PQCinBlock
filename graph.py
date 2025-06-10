import sys
import argparse
import oqs
import numpy as np

from visualization.graph import generate_graphs
import utils

def main():

    parser = argparse.ArgumentParser(
        description="Graph BlockSignPQC",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    all_algorithms = utils.load_algorithms("algorithms")
    
    parser.add_argument("--sign", help="Input list of digital signature algorithms", type=str, nargs="+", choices=list(utils.extract_algorithms(all_algorithms)))
    parser.add_argument("--levels", "-l", help="Nist levels", type=int, choices=range(1, 6), default=(range(1,6)), nargs="+")
    parser.add_argument("--dir", type=str)

    args = parser.parse_args()

    dir_results = args.dir

    filtered_algorithms = utils.filter_algorithms(all_algorithms, args.sign, args.levels)

    combined_mechanisms = {}
    for algorithm in filtered_algorithms.values():
        combined_mechanisms.update(algorithm)


    path_csv = f"{dir_results}algorithm-runs/time-evaluation-mean-std.csv"


    # Generates the execution graphs
    generate_graphs(
        path_csv=path_csv,
        dir_results=dir_results,
        mechanisms_dict=combined_mechanisms,
        columns=[
                # ("mean_keypair", "std_keypair", "Geração de chaves"),
                ("mean_sign", "std_sign", "Assinatura"),
                ("mean_verify", "std_verify", "Verificação"),
            ],
        show_legend=True,
        values_offset=0.2,
        error_offset=1.05,
        log_xticks=np.logspace(-3, 4, num=8, base=10),
        log_xlim=(1e-3, 1e4),
        # linear_xticks=np.linspace(0, 4, num=4),
        # linear_xlim=(0, 4),
    )

    dir_simulator = f"{dir_results}simulator"

    output_blocksim_mean_std = f"{dir_simulator}/blocksim-mean-std.csv"

    # Generates the simulator graphs
    generate_graphs(
        path_csv=output_blocksim_mean_std,
        dir_results=dir_simulator,
        mechanisms_dict=combined_mechanisms,
        columns=[
            # ("mean_keypair", "std_keypair", "Geração de chaves"),
            # ("mean_sign", "std_sign", "Assinatura"),
            ("mean_verify", "std_verify", "Verificação"),
        ],
        values_offset=0.2,
        error_offset=1.05,
        log_xticks=np.logspace(-2, 4, num=7, base=10),
        log_xlim=(1e-2, 1e4),
        # linear_xticks=np.linspace(0, 4, num=6),
        # linear_xlim=(0, 4),
    )
    
if __name__ == "__main__":
    main()