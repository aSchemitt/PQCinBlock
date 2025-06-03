import argparse
import oqs

# Internal imports
from sign_python.sing import executions, list_sign
from sign_python.rules import SIG_MECHANISMS
from visualization.graph import generate_graphs
import utils

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
    parser.add_argument("--simulator", help="Simulator execution", action="store_true")
    
    args = parser.parse_args()

    print(oqs.get_enabled_sig_mechanisms())

    # print algoritmos/variantes disponíveis
    if args.list_sig:
        list_sign(levels=args.levels)
    
    else:
        if args.sig:           
            dir_results, combined_mechanisms = executions(
                signs=args.sig,
                levels=args.levels,
                runs=args.runs,
                warm_up=args.warm_up,
            )

            path_csv = f"{dir_results}/time-evaluation-mean-std.csv"

            generate_graphs(
                path_csv=path_csv,
                dir_results=dir_results,
                mechanisms_dict=combined_mechanisms
            )

        if args.simulator:
            print('run simulator...')
            # passar no csv para o simulador
            # pegar csv da saída do simulador

        # gerar gráficos do simulador


if __name__ == "__main__":
    main()