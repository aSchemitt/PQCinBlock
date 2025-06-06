import pandas as pd
import numpy as np

# Internal imports
from visualization import plots
import save

def generate_graphs(
    path_csv,
    dir_results,
    mechanisms_dict,
    log_yticks,
    log_ylim,
    log_values_position,
    log_error_position,
    linear_yticks,
    linear_ylim,
    linear_values_position,
    linear_error_position,
):

    try:
        df = pd.read_csv(path_csv)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    dir_graph_log, dir_graph_linear = save.graph_dirs(dir_results)
    
    print(dir_graph_log)
    print(dir_graph_linear)

    columns=[
        # ("mean_keypair", "std_keypair", "Geração de chaves"),
        # ("mean_sign", "std_sign", "Assinatura"),
        ("mean_verify", "std_verify", "Verificação"),
    ]

    plots.generate_plots_from_csv(
        path_csv=path_csv,
        variants_dict=mechanisms_dict,
        dir_graph=dir_graph_log,
        columns = columns,
        yscale="log",
        yticks=log_yticks,
        ylim=log_ylim,
        values_position=log_values_position,
        error_position=log_error_position,
        show_graph=False,                
        show_values=True,
        show_erros=True,
        show_legend=False, 
    )

    plots.generate_plots_from_csv(
        path_csv=path_csv,
        variants_dict=mechanisms_dict,
        dir_graph=dir_graph_linear,
        columns = columns,
        yscale="linear",
        yticks=linear_yticks,
        ylim=linear_ylim,
        values_position=linear_values_position,
        error_position=linear_error_position,
        show_graph=False,                
        show_values=True,
        show_erros=True,
        show_legend=False, 
    )
