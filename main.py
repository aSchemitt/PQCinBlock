import argparse
import oqs
import pandas as pd
import numpy as np

# Internal imports
from sign_python.sing import executions, list_sign
from sign_python.rules import SIG_MECHANISMS
from visualization.graph import generate_graphs
import utils
import save
from simulator import simulator

def main():

    parser = argparse.ArgumentParser(
        description="BlockSignPQC",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--sig", help="Input list of digital signature algorithms", type=str, nargs="+", choices=list(SIG_MECHANISMS.keys()))
    parser.add_argument("--levels", "-l", help="Nist levels", type=int, choices=range(1, 6), default=(range(1,6)), nargs="+")
    parser.add_argument("--runs", "-r", help="Number of executions", type=utils.positive_int, default=1)
    parser.add_argument("--warm-up", "-wp", help="Number of executions warm up", type=utils.non_negative_int, default=0)
    parser.add_argument("--list-sig", help="List of variants digital signature algorithms", action="store_true")
    # parser.add_argument("--simulator", help="Simulator execution", action="store_true")
    parser.add_argument("--runs-simulator", help="Number of simulator runs", type=utils.non_negative_int, default=0)
    
    args = parser.parse_args()

    # Prints the available algorithms/variants
    if args.list_sig:
        list_sign(levels=args.levels)
    
    else:
        if args.sig:
            print("Algorithm run...")

            dir_results, combined_mechanisms = executions(
                signs=args.sig,
                levels=args.levels,
                runs=args.runs,
                warm_up=args.warm_up,
                log_yticks=np.logspace(-2, 1, num=4, base=10),
                log_ylim=(1e-2, 1e1),
                log_values_position=1.5e-2,
                log_error_position=1.1,
                linear_yticks=np.linspace(0, 1.4, num=4),
                linear_ylim=(0, 1.4),
                linear_values_position=0.02,
                linear_error_position=1.005,
            )

            path_csv = f"{dir_results}/time-evaluation-mean-std.csv"

            # Generates the execution graphs
            generate_graphs(
                path_csv=path_csv,
                dir_results=dir_results,
                mechanisms_dict=combined_mechanisms
            )

        if args.runs_simulator:
            print("BlockSim run...")

            output_blocksim_mean_std, dir_simulator = simulator(
                dir_results=dir_results,                 
                input_file=path_csv, 
                runs=args.runs_simulator,
            )
            
            # Generates the simulator graphs
            generate_graphs(
                path_csv=output_blocksim_mean_std,
                dir_results=dir_simulator,
                mechanisms_dict=combined_mechanisms,
                log_yticks=np.logspace(-2,3, num=6, base=10),
                log_ylim=(1e-2, 1e3),
                log_values_position=1.5e-2,
                log_error_position=1.0,
                linear_yticks=np.linspace(0, 1.4, num=6),
                linear_ylim=(0, 200),
                linear_values_position=5.0,
                linear_error_position=1.0,
            )
        
if __name__ == "__main__":
    main()