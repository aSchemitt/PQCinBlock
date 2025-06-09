import pandas as pd
import oqs

# Internal imports
from sign_python import utils
import save
from sign_python.rules import SIG_MECHANISMS, CURVES
from utils import compute_mean_std

def _run_times(mechanisms, oqs_time_evaluation, runs, warm_up, ecdsa_time_evaluation=None):

    results_times = []
    for mechanism, variants in mechanisms.items():
        if mechanism == "ecdsa":
            for variant in variants.values():
                results_times.append(ecdsa_time_evaluation(variant=variant, runs=runs, warm_up=warm_up))
        else:
            for variant in variants.values():
                results_times.append(oqs_time_evaluation(variant=variant, runs=runs, warm_up=warm_up))

    return pd.concat(results_times)


def print_variants(combined_mechanisms):

    for mechanism, variants in combined_mechanisms.items():
        print(f"{mechanism}:")
        for level, variant in variants.items():
            print(f"{4 * ' '}{variant} - NIST Level {level}")


def combines_mechanisms(
    input_mechanisms,
    oqs_mechanisms,
    normalizer,
    nist_levels,
    oqs_cls
): 

    pqc_mechanisms_groups = utils.get_pqc_mechanisms_groups(
        input_mechanisms=input_mechanisms,
        mechanisms=oqs_mechanisms(),
        normalizer=normalizer,
        nist_levels=nist_levels,
        oqs_cls=oqs_cls
    )

    ecdsa_mechanisms_groups = {}
    if 'ecdsa' in input_mechanisms:
        ecdsa_mechanisms_groups = utils.get_ecdsa_mechanisms_groups(
            input_mechanisms= input_mechanisms,
            curves=CURVES,
            nist_levels=nist_levels
        )

    combined = {}
    for mechanism in input_mechanisms:
        if mechanism in pqc_mechanisms_groups:
            combined[mechanism] = pqc_mechanisms_groups[mechanism]
        elif ecdsa_mechanisms_groups and mechanism in ecdsa_mechanisms_groups:
            combined[mechanism] = ecdsa_mechanisms_groups[mechanism]

    return combined

def executions(
    combined_mechanisms,
    input_mechanisms,
    nist_levels,
    runs,
    warm_up,
    oqs_time_evaluation=None,
    ecdsa_time_evaluation=None,
):
    # time evaluation
    df_time_evaluation = _run_times(
        mechanisms=combined_mechanisms,
        oqs_time_evaluation=oqs_time_evaluation,
        ecdsa_time_evaluation=ecdsa_time_evaluation,
        runs=runs,
        warm_up=warm_up
    )

    # Compute mean and std of time evaluation
    df_time_evaluation_mean_std = compute_mean_std(
        df=df_time_evaluation,
        group_by='variant',
        columns=[
            "keypair",
            "sign",
            "verify"
        ]
    )
    
    dfs = {
        f"time-evaluation-{runs}x": df_time_evaluation,
        "time-evaluation-mean-std": df_time_evaluation_mean_std,
    }

    dir_results = save.save_results(
        dfs=dfs,
        input_mechanisms=input_mechanisms,
        levels=nist_levels,
        mechanisms_dict=combined_mechanisms,
    )

    return dir_results

if __name__ == "__main__":
    main()