def get_variants_by_level(df, variant_dict):
    csv_variants = set(df.index.to_list())

    variants_by_level = {}

    for scheme, levels in variant_dict.items():
        for level, variant_name in levels.items():
            if variant_name in csv_variants:
                variants_by_level.setdefault(level, []).append(variant_name)

    return dict(sorted(variants_by_level.items()))
