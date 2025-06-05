import pandas as pd

def positive_int(value: int):
    """
    Validates that the provided value is a positive integer.

    Parameters:
        value (int): The value to validate.

    Returns:
        int: The validated positive integer.

    Raises:
        argparse.ArgumentTypeError: If the value is not a positive integer.
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue

def non_negative_int(value: int):
    """
    Validates that the provided value is a non-negative integer.

    Parameters:
        value (int): The value to validate.

    Returns:
        int: The validated non-negative integer.

    Raises:
        argparse.ArgumentTypeError: If the value is negative.
    """
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} is not a non-negative integer")
    return ivalue

def compute_mean_std(df, group_by, columns):
    """
    Compute mean and standard deviation for specified columns grouped by a key.

    Parameters:
    - df: The input DataFrame.
    - group_by: Column name to group by (e.g., 'variant').
    - columns: List of column names to compute mean and std for.

    Returns:
    - pd.DataFrame: DataFrame with mean and std columns.
    """
    grouped = df.groupby(group_by)

    result = pd.DataFrame()
    for col in columns:
        result[f'mean_{col}'] = grouped[col].mean()
        result[f'std_{col}'] = grouped[col].std()

    # Transform the index into a column
    result = result.reset_index()
    return result