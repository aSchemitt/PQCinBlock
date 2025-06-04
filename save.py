from os import path, makedirs
from datetime import datetime

DIR_RESULTS = "results"
DIR_GRAPH = "graph"
DIR_SIMULATOR = "simulator"

def _create_result_dirs(suffix=None):
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    dir_name = f"{timestamp}_{suffix}" if suffix else timestamp

    dir_results = path.join(DIR_RESULTS, dir_name)

    makedirs(dir_results, exist_ok=True)

    return dir_results 

def _save_csv(df, file):
    df.to_csv(file, index=False)
    print(file)
    # print(f"File {file} was created")

def graph_dirs(dir_results):

    dir_graph = path.join(dir_results, DIR_GRAPH)
    
    dir_graph_log = path.join(dir_graph, "log")
    dir_graph_linear = path.join(dir_graph, "linear")

    makedirs(dir_graph_log, exist_ok=True)
    makedirs(dir_graph_linear, exist_ok=True)

    return dir_graph_log, dir_graph_linear

def simulator_dir(dir_results):
    
    dir_simulator = path.join(dir_results, DIR_SIMULATOR)

    makedirs(dir_simulator, exist_ok=True)

    return dir_simulator

def save_results(dfs, input_mechanisms, levels, mechanisms_dict=None):

    mechanisms_str = "_".join(input_mechanisms)

    levels_str = "-".join(map(str, levels))

    dir_results = _create_result_dirs(f"{mechanisms_str}_levels-{levels_str}")

    for key, df in dfs.items():

        f = dir_results.split("/")
        file = f"{dir_results}/{key}.csv"
        _save_csv(df, file)
    
    return dir_results

