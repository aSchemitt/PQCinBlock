def get_variants_by_level(df, variant_dict):
    csv_variants = set(df.index.to_list())
    variants_by_level = {}

    for algorithm, levels in variant_dict.items():
        for level, variant in levels.items():
            if variant in csv_variants:
                variants_by_level.setdefault(level, []).append({
                    "algorithm": algorithm,
                    "variant": variant
                })

    return dict(sorted(variants_by_level.items()))
