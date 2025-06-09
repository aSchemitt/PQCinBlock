from os import path, makedirs
from datetime import datetime

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
    
    full_path = path.join(DIR_RESULTS, base_dir)

    return full_path

def _save_csv(df, file):
    df.to_csv(file, index=False)

def _create_directory(root_directory, directory_name=None):
    if directory_name:
        directory = path.join(root_directory, directory_name)
        makedirs(directory, exist_ok=True)
        return directory
    else:
        makedirs(root_directory, exist_ok=True)
        return root_directory

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
        file = f"{algorithms_runs_directory}/{key}.csv"
        _save_csv(df, file)
        print(f"{file}")
    
    return results_directory, algorithms_runs_directory, 

