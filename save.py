from pathlib import Path
from datetime import datetime
import logging
DIR_RESULTS = "results"
DIR_ALGORITHMS_RUNS = "algorithm-runs"
DIR_GRAPH = "graph"
DIR_SIMULATOR = "simulator"

def _mounts_results_directory(algorithms_dict, levels):
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    mechanisms = set()
    for module_mechanisms in algorithms_dict.values():
        mechanisms.update(module_mechanisms.keys())
    mechanisms_str = "_".join(sorted(mechanisms))

    levels_str = "-".join(str(level) for level in sorted(levels))

    base_dir = f"{timestamp}_{mechanisms_str}_levels-{levels_str}"
    
    full_path = Path(DIR_RESULTS) / base_dir

    return full_path

def _save_csv(df, file):
    df.to_csv(file, index=False)

def _create_directory(root_directory, directory_name=None):
    if directory_name:
        directory = Path(root_directory) / directory_name
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    else:
        Path(root_directory).mkdir(parents=True, exist_ok=True)
        return Path(root_directory)

def create_results_directory(algorithms_dict, levels):
    results_directory = _mounts_results_directory(algorithms_dict, levels)
    return _create_directory(results_directory)

def create_algorithms_runs_directory(root_directory):
    return _create_directory(root_directory, DIR_ALGORITHMS_RUNS)

def create_graphics_directory(root_directory):
    return _create_directory(root_directory, DIR_GRAPH)

def create_simulator_directory(root_directory):
    return _create_directory(root_directory, DIR_SIMULATOR)

def save_results_algorithm_runs(dfs, algorithms_dict, levels):

    results_directory = create_results_directory(
        algorithms_dict=algorithms_dict,
        levels=levels
    )
    algorithms_runs_directory = create_algorithms_runs_directory(results_directory)
    
    for key, df in dfs.items():
        file = algorithms_runs_directory / f"{key}.csv"
        _save_csv(df, file)
        logging.info(f"\t\t{file}")
    
    return results_directory, algorithms_runs_directory