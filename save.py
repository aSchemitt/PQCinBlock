from os import path, makedirs
from datetime import datetime

DIR_RESULTS = "results"
DIR_EXECUTIONS = "executions"
DIR_GRAPH = "graph"
DIR_SIMULATOR = "simulator"

def _create_result_dirs(algorithms_dict, levels):
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    mechanisms = set()
    for module_mechanisms in algorithms_dict.values():
        mechanisms.update(module_mechanisms.keys())
    mechanisms_str = "_".join(sorted(mechanisms))

    levels_str = "-".join(str(level) for level in sorted(levels))

    base_dir = f"{timestamp}_{mechanisms_str}_levels-{levels_str}"
    full_path = path.join(DIR_RESULTS, base_dir, DIR_EXECUTIONS)

    makedirs(full_path, exist_ok=True)

    return full_path

def _save_csv(df, file):
    df.to_csv(file, index=False)

def create_directory(dir_results, directory_name):
    directory = path.join(dir_results, directory_name)
    makedirs(directory, exist_ok=True)
    return directory

def create_graphics_directory(dir_results):
    return create_directory(dir_results, DIR_GRAPH)

def create_simulator_directory(dir_results):
    return create_directory(dir_results, DIR_SIMULATOR)

def save_results(dfs, algorithms_dict, levels):

    dir_results = _create_result_dirs(
        algorithms_dict=algorithms_dict,
        levels=levels
    )

    print("\nFiles created:")
    for key, df in dfs.items():
        f = dir_results.split("/")
        file = f"{dir_results}/{key}.csv"
        _save_csv(df, file)
        print(f"{file}")
    
    return dir_results

