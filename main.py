import argparse
import oqs
import pandas as pd
import numpy as np

# Internal imports
from sign_python.sing import executions, print_variants, combines_mechanisms
from algorithms import pqc, ecdsa
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
    
    parser.add_argument("--sign", help="Input list of digital signature algorithms", type=str, nargs="+", choices=list(SIG_MECHANISMS.keys()))
    parser.add_argument("--levels", "-l", help="Nist levels", type=int, choices=range(1, 6), default=(range(1,6)), nargs="+")
    parser.add_argument("--runs", "-r", help="Number of executions", type=utils.positive_int, default=1)
    parser.add_argument("--warm-up", "-wp", help="Number of executions warm up", type=utils.non_negative_int, default=0)
    parser.add_argument("--list-sign", help="List of variants digital signature algorithms", action="store_true")
    # parser.add_argument("--simulator", help="Simulator execution", action="store_true")
    parser.add_argument("--runs-simulator", help="Number of simulator runs", type=utils.non_negative_int, default=0)
    
    args = parser.parse_args()

    # Prints the available algorithms/variants
    if args.list_sign:
        combined_mechanisms = combines_mechanisms(
            input_mechanisms=SIG_MECHANISMS.keys(),
            oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
            normalizer=SIG_MECHANISMS,
            nist_levels=args.levels,
            oqs_cls=oqs.Signature
        )

        print_variants(combined_mechanisms)
    
    else:
        if args.sign:
            print("Algorithm run...")

            combined_mechanisms = combines_mechanisms(
                input_mechanisms=args.sign,
                oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
                normalizer=SIG_MECHANISMS,
                nist_levels=args.levels,
                oqs_cls=oqs.Signature
            )

            dir_results = executions(
                combined_mechanisms=combined_mechanisms,
                input_mechanisms=args.sign,
                nist_levels=args.levels,
                runs=args.runs,
                warm_up=args.warm_up,
                oqs_time_evaluation=pqc.time_evaluation,
                ecdsa_time_evaluation=ecdsa.time_evaluation,
            )

            path_csv = f"{dir_results}/time-evaluation-mean-std.csv"

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