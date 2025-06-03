import pandas as pd
import numpy as np

# Internal imports
from visualization import plots
import save

def generate_graphs(
    path_csv,
    dir_results,
    mechanisms_dict,
    # TODO outros parametros de entrada
    ):

    try:
        df = pd.read_csv(path_csv)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    dir_graph_log, dir_graph_linear = save.graph_dirs(dir_results)
    
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
        yticks=np.logspace(-2, 1, num=4, base=10), # log
        ylim=(1e-2, 1e1), # log
        values_position=1.5e-2, #log
        error_position=1.1, #log        
        show_graph=True,                
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
        yticks=np.linspace(0, 1.4, num=4), # linear
        ylim=(0, 1.4), # linear
        values_position=0.02, #linear
        error_position=1.005, #linear
        show_graph=True,                
        show_values=True,
        show_erros=True,
        show_legend=False, 
    )



if __name__ == "__main__":
    main()