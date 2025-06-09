import argparse
import oqs
import pandas as pd
import numpy as np

# Internal imports
# from sign_python.sing import executions, combines_mechanisms
# from sign_python.rules import SIG_MECHANISMS
# from visualization.graph import generate_graphs
import sign_python as sign
import utils
from  simulator import simulator

def main():

    parser = argparse.ArgumentParser(
        description="BlockSignPQC",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    all_algorithms = utils.load_algorithms("algorithms")
    
    parser.add_argument("--sign", help="Input list of digital signature algorithms", type=str, nargs="+", choices=list(utils.extract_algorithms(all_algorithms)))
    parser.add_argument("--levels", "-l", help="Nist levels", type=int, choices=range(1, 6), default=(range(1,6)), nargs="+")
    parser.add_argument("--runs", "-r", help="Number of executions", type=utils.positive_int, default=1)
    parser.add_argument("--warm-up", "-wp", help="Number of executions warm up", type=utils.non_negative_int, default=0)
    parser.add_argument("--list-sign", help="List of variants digital signature algorithms", action="store_true")
    parser.add_argument("--runs-simulator", help="Number of simulator runs", type=utils.non_negative_int, default=0)
    
    args = parser.parse_args()
    
    filtered_algorithms = utils.filter_algorithms(all_algorithms, args.sign, args.levels)

    if args.list_sign:
        sign.print_by_variants(filtered_algorithms)

    if args.sign:
        print("\nAlgorithms run...")

        evaluations_functions = utils.load_functions("algorithms")

        dir_results, path_csv = sign.executions(
            levels=args.levels,
            variants_by_module=filtered_algorithms,
            evaluations_functions=evaluations_functions,
            runs=args.runs,
            warm_up=args.warm_up
        )
    
        if args.runs_simulator:
            print("\nBlockSim run...")
            
            simulator(
                dir_results=dir_results,                 
                input_file=path_csv, 
                runs=args.runs_simulator,
                variants_by_module=filtered_algorithms,
            )
        
if __name__ == "__main__":
    main()