import pandas as pd

# Internal imports
from save import simulator_dir
from utils import compute_mean_std
from BlockSim.Main import blocksim

def simulator(dir_results, input_file, runs):

    dir_simulator = simulator_dir(dir_results=dir_results)
    
    output_blocksim=f"{dir_simulator}/blocksim-{runs}x.csv"
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

    output_blocksim_mean_std = f"{dir_simulator}/blocksim-mean-std.csv"

    print(output_blocksim)
    print(output_blocksim_mean_std)

    df_simulator_mean_std.to_csv(output_blocksim_mean_std, index=False)

    return output_blocksim_mean_std, dir_simulator