import argparse
import pandas as pd
from pathlib import Path
import os

# Internal imports
import sign_python as sign
import utils
import save
import info

# Constants
VARIANT_COLUMN = 'variant'
ALGORITHMS_DIR = 'algorithms'

def _get_combined_mechanisms(filtered_algorithms):
    """Get a combined dictionary of all algorithm variants."""
    combined_mechanisms = {}
    for algorithm in filtered_algorithms.values():
        combined_mechanisms.update(algorithm)
    return combined_mechanisms

def _run_simulator_from_input_file(args, filtered_algorithms, parser):
    """Handles the logic when the script is run with an input file."""
    from simulator import simulator
    import graph

    if not args.runs_simulator:
        parser.error("--runs-simulator must be provided with --input-file.")

    print("\nBlockSim run from input file...")

    try:
        input_path = Path(args.input_file)
        if not input_path.is_file():
            raise FileNotFoundError(f"Input file not found at: {input_path}")
        df = pd.read_csv(input_path)
        if VARIANT_COLUMN not in df.columns:
            raise KeyError(f"Column '{VARIANT_COLUMN}' not found in the input file.")
        variants_in_file = set(df[VARIANT_COLUMN].unique())
    except (FileNotFoundError, pd.errors.EmptyDataError, KeyError) as e:
        print(f"Error processing input file '{args.input_file}': {e}")
        return

    if not filtered_algorithms:
        print("No algorithms left after filtering. Please check your --sign and --level arguments.")
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
        print("\nWarning: The following algorithms from --sign were not found in the input CSV and will be ignored:")
        for variant in sorted(list(missing_variants)):
            print(f"- {variant}")

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

    info.export_metadata(format="json", filename=Path(dir_results) / "metadata.json")

    dir_results_path = Path(dir_results)
    filtered_csv_path = dir_results_path / "filtered-input.csv"
    df_filtered.to_csv(filtered_csv_path, index=False)
    print(f"Filtered data saved to: {filtered_csv_path}")

    simulator(
        dir_results=dir_results,
        input_file=str(filtered_csv_path),
        runs=args.runs_simulator,
        variants_by_module=filtered_algorithms,
    )

    graph.generate_all_graphs(
        dir_results=dir_results,
        mechanisms_dict=_get_combined_mechanisms(filtered_algorithms),
        simulator_was_run=True
    )

def _run_from_sign_algorithms_and_simulator(args, filtered_algorithms):
    """Handles the logic when the script is run with --sign arguments."""
    import graph

    print("\nAlgorithms run...")

    evaluations_functions = utils.load_functions(ALGORITHMS_DIR)

    dir_results, path_csv = sign.executions(
        levels=args.levels,
        variants_by_module=filtered_algorithms,
        evaluations_functions=evaluations_functions,
        runs=args.runs,
        warm_up=args.warm_up
    )

    info.export_metadata(format="json", filename=Path(dir_results) / "metadata.json")

    simulator_was_run = args.runs_simulator > 0
    if simulator_was_run:
        from simulator import simulator
        print("\nBlockSim run...")
        simulator(
            dir_results=dir_results,
            input_file=path_csv,
            runs=args.runs_simulator,
            variants_by_module=filtered_algorithms,
        )
    
    graph.generate_all_graphs(
        dir_results=dir_results,
        mechanisms_dict=_get_combined_mechanisms(filtered_algorithms),
        simulator_was_run=simulator_was_run
    )

def main():
    """Main function to parse arguments and dispatch tasks."""
    parser = argparse.ArgumentParser(
        description="BlockSignPQC",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    all_algorithms = utils.load_algorithms(ALGORITHMS_DIR)
    valid_signs = list(utils.extract_algorithms(all_algorithms))
    valid_levels = list(range(1, 6))
    
    parser.add_argument("--model", type=int, default=2, choices=[0, 1, 2, 3], help="BlockSim model to use (0: Base, 1: Bitcoin, 2: Ethereum, 3: AppendableBlock)")
    parser.add_argument("--sign", help="Input list of digital signature algorithms (space-separated)", type=str, nargs="+", choices=valid_signs)
    parser.add_argument("--levels", "-l", help="Nist levels (space-separated)", type=int, nargs="+", default=valid_levels, choices=valid_levels)
    parser.add_argument("--runs", "-r", help="Number of executions", type=utils.positive_int, default=1)
    parser.add_argument("--warm-up", "-wp", help="Number of executions warm up", type=utils.non_negative_int, default=0)
    parser.add_argument("--list-sign", help="List of variants digital signature algorithms", action="store_true")
    parser.add_argument("--runs-simulator", help="Number of simulator runs", type=utils.non_negative_int, default=0)
    parser.add_argument("--input-file", help="Input CSV file for the simulator to run independently.", type=str)
    
    args = parser.parse_args()

    # Set environment variable for BlockSim model before importing the simulator
    os.environ['BLOCKSIM_MODEL'] = str(args.model)
    
    filtered_algorithms = utils.filter_algorithms(all_algorithms, args.sign, args.levels)

    if args.input_file:
        _run_simulator_from_input_file(args, filtered_algorithms, parser)
    elif args.sign:
        _run_from_sign_algorithms_and_simulator(args, filtered_algorithms)
    elif args.list_sign:
        sign.print_by_variants(filtered_algorithms)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()