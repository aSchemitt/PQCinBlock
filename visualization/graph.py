import pandas as pd
import numpy as np

# Internal imports
from visualization import plots
import save

def generate_graphs(
    path_csv,
    dir_results,
    columns,
    mechanisms_dict,
    values_offset,
    error_offset,
    log_xticks,
    log_xlim,
    linear_xticks,
    linear_xlim,
    show_graph=False,
    show_values=True,
    show_erros=True,
    show_legend=False, 
):

    try:
        df = pd.read_csv(path_csv)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    dir_graph_log, dir_graph_linear = save.graph_dirs(dir_results)
    
    print(dir_graph_log)
    # print(dir_graph_linear)

    plots.generate_plots_from_csv(
        path_csv=path_csv,
        variants_dict=mechanisms_dict,
        dir_graph=dir_graph_log,
        columns = columns,
        xscale="log",
        xticks=log_xticks,
        xlim=log_xlim,
        values_offset=values_offset,
        error_offset=error_offset,
        show_graph=show_graph,                
        show_values=show_values,
        show_erros=show_erros,
        show_legend=show_legend, 
    )

    # plots.generate_plots_from_csv(
    #     path_csv=path_csv,
    #     variants_dict=mechanisms_dict,
    #     dir_graph=dir_graph_linear,
    #     columns = columns,
    #     xscale="linear",
    #     xticks=linear_xticks,
    #     xlim=linear_xlim,
    #     values_offset=values_offset,
    #     error_offset=error_offset,
    #     show_graph=False,                
    #     show_values=True,
    #     show_erros=True,
    #     show_legend=False, 
    # )
