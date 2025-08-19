import argparse
from datetime import datetime
import pandas as pd
from pathlib import Path

# Internal imports
import sign_python as sign
import utils
import save
import info
import graph
import sys
from colorama import init, Fore, Style
import logging
from logging.handlers import RotatingFileHandler

from simulator import simulator

# Constants
VARIANT_COLUMN = 'variant'
ALGORITHMS_DIR = 'algorithms'

def _print_all_settings(arguments):
    """Logs the full configuration of the current experiment based on parsed arguments."""
    logging.info("Command:\n\t{0}\n".format(" ".join([x for x in sys.argv])))
    logging.info("Settings:")
    lengths = [len(x) for x in vars(arguments).keys()]
    max_length = max(lengths)

    for key_item, values in sorted(vars(arguments).items()):
        message = "\t"
        message += key_item.ljust(max_length, " ")
        message += " : {}".format(values)
        logging.info(message)

    logging.info("")

def _get_combined_mechanisms(filtered_algorithms):
    """Get a combined dictionary of all algorithm variants."""
    combined_mechanisms = {}
    for algorithm in filtered_algorithms.values():
        combined_mechanisms.update(algorithm)
    return combined_mechanisms

def _export_input_and_system_info(args, dir_results):
    info.export_metadata(
        args,
        format="json",
        filename=Path(dir_results) / "input-and-system-info.json"
    )

def _run_simulator_only(args, filtered_algorithms, parser):

    try:
        input_path = Path(args.input_file)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input file not found at: {input_path}")
        df = pd.read_csv(input_path)
        if VARIANT_COLUMN not in df.columns:
            raise KeyError(f"Column '{VARIANT_COLUMN}' not found in the input file.")
        variants_in_file = set(df[VARIANT_COLUMN].unique())

    except (FileNotFoundError, pd.errors.EmptyDataError, KeyError) as e:
        logging.error(f"Error processing input file '{args.input_file}': {e}")
        return

    if not filtered_algorithms:
        logging.error("No algorithms left after filtering. Please check your --sign and --level arguments.")
        return

    variants_to_keep = [
        variant
        for module_algos in filtered_algorithms.values()
        for algo_variants in module_algos.values()
        for variant in algo_variants.values()
    ]

    sign_variants_set = set(variants_to_keep)
    missing_variants = sign_variants_set - variants_in_file

    if missing_variants:
        logging.warning("\nWarning: The following algorithms from --sign were not found in the input CSV and will be ignored:")
        for variant in sorted(list(missing_variants)):
            logging.info(f"\t- {variant}")

    df_filtered = df[df[VARIANT_COLUMN].isin(variants_to_keep)]

    levels_present = {
        level
        for module_algos in filtered_algorithms.values()
        for algo_variants in module_algos.values()
        for level in algo_variants.keys()
    }

    dir_results = save.create_results_directory(
        algorithms_dict=filtered_algorithms,
        levels=sorted(list(levels_present))
    )

    _export_input_and_system_info(args, dir_results)

    dir_results_path = Path(dir_results)
    filtered_csv_path = dir_results_path / "filtered-input.csv"
    df_filtered.to_csv(filtered_csv_path, index=False)
    logging.info(f"Filtered data saved to: {filtered_csv_path}")

    _run_simulator(args, filtered_algorithms, dir_results, path_csv=filtered_csv_path)


def _run_benchmark(args, filtered_algorithms):
    """Handles the logic when the script is run with --sign arguments."""

    logging.info(Fore.BLUE)
    logging.info("\nBenchmark run...\n")

    evaluations_functions = utils.load_functions(ALGORITHMS_DIR)

    dir_results, path_csv = sign.executions(
        levels=args.levels,
        variants_by_module=filtered_algorithms,
        evaluations_functions=evaluations_functions,
        runs=args.runs,
        warm_up=args.warm_up
    )

    _export_input_and_system_info(args, dir_results)

    graph.generate_benchmark_graphs(
        dir_results=dir_results,
        path_csv_benchmark=path_csv,
        mechanisms_dict=_get_combined_mechanisms(filtered_algorithms),
    )

    return dir_results, path_csv

def _run_simulator(args, filtered_algorithms, dir_results, path_csv):

    logging.info(Fore.GREEN)

    simulator_was_run = args.runs_simulator > 0
    if simulator_was_run:        
        print("\nBlockSim run...")
        for model in args.model:                    
            path_csv_simulator = simulator(
                dir_results=dir_results,
                model=model,
                input_file=path_csv,
                runs=args.runs_simulator,
                variants_by_module=filtered_algorithms,
            )

        graph.generate_simulator_graphs (
            dir_results=dir_results,
            path_csv_simulator=path_csv_simulator,
            mechanisms_dict=_get_combined_mechanisms(filtered_algorithms),
            simulator_was_run=simulator_was_run
        )


def _run_benchmark_and_simulator(args, filtered_algorithms):
    dir_results, path_csv = _run_benchmark(args, filtered_algorithms)
    _run_simulator(args, filtered_algorithms, dir_results, path_csv)


def main():
    """Main function to parse arguments and dispatch tasks."""
    parser = argparse.ArgumentParser(
        description="BlockSignPQC",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    all_algorithms = utils.load_algorithms(ALGORITHMS_DIR)
    valid_signs = list(utils.extract_algorithms(all_algorithms))
    valid_levels = list(range(1, 6))
    
    parser.add_argument("--model", "-m", type=int, nargs="+", default=[2], choices=[1, 2], help="BlockSim model to use (1: Bitcoin, 2: Ethereum)")
    parser.add_argument("--sign", "-s", help="Input list of digital signature algorithms (space-separated)", type=str, nargs="+", choices=valid_signs)
    parser.add_argument("--levels", "-l", help="Nist levels (space-separated)", type=int, nargs="+", default=valid_levels, choices=valid_levels)
    parser.add_argument("--runs", "-r", help="Number of executions", type=utils.positive_int, default=1)
    parser.add_argument("--warm-up", "-wp", help="Number of executions warm up", type=utils.non_negative_int, default=0)
    parser.add_argument("--list-sign", help="List of variants digital signature algorithms", action="store_true")
    parser.add_argument("--runs-simulator", help="Number of simulator runs", type=utils.non_negative_int, default=0)
    parser.add_argument("--input-file", "-i", help="Input CSV file for the simulator to run independently of benchmark.", type=str)
    help_msg = "verbosity logging level (INFO=%d DEBUG=%d)" % (logging.INFO, logging.DEBUG)
    parser.add_argument("--verbosity", "-v", help=help_msg, default=logging.INFO, type=int)

    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logging_filename = f'./log_{timestamp}.log'

    logging_format = '%(asctime)s\t---\t%(message)s'

    if args.verbosity == logging.DEBUG:
        logging_format = '%(asctime)s\t---\t%(levelname)s {%(module)s} [%(funcName)s] %(message)s'

     

    # formatter = logging.Formatter(logging_format, datefmt=TIME_FORMAT, level=args.verbosity)
    logging.basicConfig(format=logging_format, level=args.verbosity)

    # Add file rotating handler, with level DEBUG
    rotatingFileHandler = RotatingFileHandler(filename=logging_filename, maxBytes=100000, backupCount=5)
    rotatingFileHandler.setLevel(args.verbosity)
    rotatingFileHandler.setFormatter(logging.Formatter(logging_format))
    logging.getLogger().addHandler(rotatingFileHandler)

    _print_all_settings(args)


    filtered_algorithms = utils.filter_algorithms(all_algorithms, args.sign, args.levels)

    if args.list_sign:
        sign.print_by_variants(filtered_algorithms)        
    elif args.input_file:
        if not args.runs_simulator:
            parser.error("--runs-simulator must be provided with --input-file.")
        else:
            _run_simulator_only(args, filtered_algorithms, parser)
    elif args.sign:
        _run_benchmark_and_simulator(args, filtered_algorithms)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()