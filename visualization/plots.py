import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd

# Internal import 
from visualization import utils

def plot_horizontal(
    df_all, 
    columns,
    dir_graph,
    values_offset,
    error_offset,
    level, 
    xscale,
    xlabel,
    xlim,
    xticks, 
    yticklabels,
    figsize, 
    width,
    title=None,
    ylabel=None,
    show_graph=False,
    show_values=True,
    show_errors=True,
    show_legend=True,
    save_formats=("svg", "png")
):
    n_variants = len(df_all)
    n_columns = len(columns)
    
    width_bar = width / n_columns

    y = np.arange(n_variants)

    fig, ax = plt.subplots(figsize=figsize)

    palette = sns.color_palette("muted", n_colors=n_columns)

    for i, (val_col, err_col, label) in enumerate(columns):
        values = df_all[val_col]
        errors = df_all[err_col]
        
        reverse_i = n_columns - 1 - i

        bars = ax.barh(
            y + (reverse_i - (n_columns - 1) / 2) * width_bar,
            values,
            height=width_bar,
            xerr=errors if show_errors else None,
            label=label,
            color=palette[i],
            error_kw={"capsize": 5, "ecolor": "red", "elinewidth": 2}
        )

        # values
        if show_values:
            for bar, value in zip(bars, values):
                offset = values_offset
                ax.text(
                    value * (1 - offset),
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.3f}",    
                    va="center_baseline",
                    ha="right",
                    fontsize=22,
                    color="black",
                    fontweight=600,
                )

        # error
        if show_errors:
            for bar, value, error in zip(bars, values, errors):
                right = value + error
                offset = error_offset
                ax.text(
                    right * offset,
                    bar.get_y() + bar.get_height() / 2,
                    f"±{error:.3f}",
                    va="center_baseline",
                    ha="left",
                    fontsize=20,
                    color="red",
                )

    ax.set_yticks(y)
    ax.set_yticklabels(df_all[yticklabels].to_list(), rotation=0, va="center")

    if ylabel:
        ax.set_ylabel(ylabel, fontsize=24)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=24)
    if title:
        ax.set_title(title, fontsize=32)

    ax.set_xscale(xscale)
    
    if xscale == "log":
        ax.set_xticks(xticks)
    
    if xscale == "linear" and xlim:
        ax.set_xlim(*xlim)

    ax.set_ylim(y[0] - 0.5, y[-1] + 0.5)

    ax.tick_params(axis="y", labelsize=28)
    ax.tick_params(axis="x", labelsize=28)

    if show_legend:
        ax.legend(loc="upper right", fontsize=28)

    ax.grid(True, axis="x", linestyle="--", linewidth=0.5, alpha=0.7)

    plt.tight_layout()

    filename = f"level_{level}" if level else "all_level"

    for ext in save_formats:
        file = f"{dir_graph}/{filename}.{ext}"
        plt.savefig(file, format=ext)

    if show_graph:
        plt.show()
    else:
        plt.close()


def generate_plots_from_csv(
    path_csv,
    dir_graph,
    variants_dict,
    columns,
    show_graph,
    show_values,
    show_erros,
    show_legend,
    values_offset,
    error_offset,
    xscale,
    xlim,
    xticks,
    width=0.85,
    xlabel="Tempo médio (ms)",
    ylabel="Algoritmos",    
    figsize=(16, 9),
    save_formats=("svg", "png"),
):
    """
    Generates bar plots with error bars from a benchmark CSV file.

    For each level defined in `variants_dict`, this function creates a bar plot comparing
    different variants, including optional error bars, value labels, and legends.

    Args:
        path_csv (str): Path to the CSV file containing the benchmark data.
        dir_graph (str): Directory where the plots will be saved.
        variants_dict (dict): Dictionary mapping levels to lists of variants.
        columns (list[tuple]): List of tuples in the form (value_column, error_column, label) 
            representing the data to plot.
        show_graph (bool): If True, displays the plots after creation.
        show_values (bool): If True, displays the numeric values on top of the bars.
        show_erros (bool): If True, displays the error values above the bars.
        show_legend (bool): If True, displays the legend on the plot.
        ylabel (str, optional): Label for the Y-axis. Defaults to "Tempo (ms)".
        xlabel (str, optional): Label for the X-axis. Defaults to "Algoritmos".
        yscale (str, optional): Scale for the Y-axis, either "log" or "linear". Defaults to "log".
        figsize (tuple, optional): Size of the figure in inches. Defaults to (16, 9).
        save_formats (tuple, optional): File formats to save the plots (e.g., ("svg", "png")). 
            Defaults to ("svg", "png").

    Returns:
        None
    """
    
    df = pd.read_csv(path_csv, index_col="variant")

    variants_by_level = utils.get_variants_by_level(df, variants_dict)

    for level, mechanisms in variants_by_level.items():

        variant_to_algorithm = {m["variant"]: m["algorithm"] for m in mechanisms}

        variant_names = [m["variant"] for m in mechanisms]

        df_subset = df.loc[variant_names]

        df_subset["algorithm"] = df_subset.index.map(variant_to_algorithm)
        
        # plot(
        #     df_all=df_subset,
        #     columns=columns,
        #     level=level,
        #     dir_graph=dir_graph,
        #     yscale=yscale,
        #     ylabel=ylabel,
        #     ylim=ylim,
        #     yticks=yticks,
        #     values_position=values_position,
        #     error_position=error_position,
        #     figsize=figsize,
        #     title=f"Nível {level}",
        #     show_graph=show_graph,
        #     show_values=show_values,
        #     show_errors=show_erros,
        #     show_legend=show_legend,
        #     save_formats=save_formats
        # )

        plot_horizontal(
            df_all=df_subset, 
            columns=columns,
            dir_graph=dir_graph,
            values_offset=values_offset,
            error_offset=error_offset,
            level=level, 
            # ylabel=ylabel,
            xlabel=xlabel,
            xlim=xlim,
            xticks=xticks, 
            yticklabels="algorithm",
            figsize=figsize,
            width=width,
            xscale=xscale,
            # title=f"Nível {level}",
            show_graph=show_graph,
            show_values=show_values,
            show_errors=show_erros,
            show_legend=show_legend,
            save_formats=("svg", "png")
        )