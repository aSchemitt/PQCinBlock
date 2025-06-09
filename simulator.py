import pandas as pd
import numpy as np

# Internal imports
import save
from utils import compute_mean_std
from BlockSim.Main import blocksim
from visualization.graph import generate_graphs

def simulator(dir_results, input_file, runs, combined_mechanisms):

    simulator_directory = save.create_simulator_directory(dir_results=dir_results)
    
    output_blocksim=f"{simulator_directory}/blocksim-{runs}x.csv"
    blocksim(input_file=input_file, output_file=output_blocksim, runs=runs)

    try:
        df = pd.read_csv(output_blocksim)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    df_simulator_mean_std = compute_mean_std(
        df=df, 
        group_by='variant', 
        columns=["verify"],
    )

    output_blocksim_mean_std = f"{simulator_directory}/blocksim-mean-std.csv"

    print(output_blocksim)
    print(output_blocksim_mean_std)

    df_simulator_mean_std.to_csv(output_blocksim_mean_std, index=False)

    # Generates the simulator graphs
    generate_graphs(
        path_csv=output_blocksim_mean_std,
        dir_results=simulator_directory,
        mechanisms_dict=combined_mechanisms,
        columns=[
            # ("mean_keypair", "std_keypair", "Geração de chaves"),
            # ("mean_sign", "std_sign", "Assinatura"),
            ("mean_verify", "std_verify", "Verificação"),
        ],
        values_offset=0.2,
        error_offset=1.05,
        log_xticks=np.logspace(-2, 4, num=7, base=10),
        log_xlim=(1e-2, 1e4),
    )