import pandas as pd
import oqs

# Internal imports
from sign_python import pqc, ecdsa, utils
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


def _print_variants(input_mechanisms, oqs_mechanisms, normalizer, nist_levels, oqs_cls, ecds_mechanisms=None):

    combined_mechanisms = combines_mechanisms(
        input_mechanisms=input_mechanisms,
        oqs_mechanisms=oqs_mechanisms,
        normalizer=normalizer,
        nist_levels=nist_levels,
        oqs_cls=oqs_cls
    )

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

def _evaluation(
    input_mechanisms,
    oqs_mechanisms,
    normalizer,
    nist_levels,
    oqs_cls,
    runs,
    warm_up,
    oqs_time_evaluation=None,
    ecdsa_time_evaluation=None,
):
    combined_mechanisms = combines_mechanisms(
        input_mechanisms=input_mechanisms,
        oqs_mechanisms=oqs_mechanisms,
        normalizer=normalizer,
        nist_levels=nist_levels,
        oqs_cls=oqs_cls
    )

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
            # "keypair",
            # "sign",
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

    return dir_results, combined_mechanisms

def list_sign(levels):

    print("Digital Signature")
    # print(oqs.get_enabled_sig_mechanisms())
    # print(oqs.get_supported_sig_mechanisms()) 

    _print_variants(
        input_mechanisms=SIG_MECHANISMS.keys(),
        oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
        normalizer=SIG_MECHANISMS,
        nist_levels=levels,
        oqs_cls=oqs.Signature
    )


def executions(
    signs,
    levels,
    runs,
    warm_up,
):
    dir_results, combined_mechanisms = _evaluation(
        input_mechanisms=signs,
        oqs_mechanisms=oqs.get_enabled_sig_mechanisms,
        normalizer=SIG_MECHANISMS,
        nist_levels=levels,
        oqs_cls=oqs.Signature,
        oqs_time_evaluation=pqc.time_evaluation,
        ecdsa_time_evaluation=ecdsa.time_evaluation,
        runs=runs,
        warm_up=warm_up,
    )

    return dir_results, combined_mechanisms

if __name__ == "__main__":
    main()