import numpy as np
from pathlib import Path

from visualization.graph import generate_graphs

def generate_all_graphs(dir_results, mechanisms_dict, simulator_was_run=False):
    """
    Generates all graphs for the experiment, including algorithm performance
    and simulator results.

    Args:
        dir_results (str or Path): The main results directory.
        mechanisms_dict (dict): A dictionary of the mechanisms used.
        simulator_was_run (bool): Flag indicating if the simulator was executed.
    """
    dir_results = Path(dir_results)
    algorithm_runs_dir = dir_results / "algorithm-runs"
    simulator_dir = dir_results / "simulator"

    # Generate graphs for algorithm performance
    path_csv_sign = algorithm_runs_dir / "time-evaluation-mean-std.csv"
    if path_csv_sign.exists():
        print("\nGenerating algorithm performance graphs...")
        generate_graphs(
            path_csv=str(path_csv_sign),
            dir_results=str(algorithm_runs_dir),
            mechanisms_dict=mechanisms_dict,
            columns=[
                ("mean_sign", "std_sign", "Creation"),
                ("mean_verify", "std_verify", "Verification"),
            ],
            show_legend=True,
            values_offset=0.2,
            error_offset=1.05,
            log_xticks=np.logspace(-3, 4, num=8, base=10),
            log_xlim=(1e-3, 1e4),
        )
    else:
        print(f"\nWarning: Algorithm CSV file not found, skipping algorithm graphs: {path_csv_sign}")

    # Generate graphs for simulator results
    path_csv_simulator = simulator_dir / "blocksim-mean-std.csv"
    if path_csv_simulator.exists():
        print("\nGenerating simulator results graphs...")
        generate_graphs(
            path_csv=str(path_csv_simulator),
            dir_results=str(simulator_dir),
            mechanisms_dict=mechanisms_dict,
            columns=[
                ("mean_verify", "std_verify", "Verification"),
            ],
            values_offset=0.2,
            error_offset=1.05,
            log_xticks=np.logspace(-2, 4, num=7, base=10),
            log_xlim=(1e-2, 1e4),
        )
    else:
        if simulator_was_run:
            print(f"\nWarning: Simulator output CSV not found, skipping simulator graphs: {path_csv_simulator}")
        else:
            print("\nSimulator not executed, skipping simulator graphs.")