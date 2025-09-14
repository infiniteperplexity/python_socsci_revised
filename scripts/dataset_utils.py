import pandas as pd
from matplotlib import pyplot as plt

## Recode values for a variable
def map_variable(
    val_or_series,
    mapping = None,
    nulls = None,
    keep = None,
    type_check = int
):
    if keep:
        keep += [str(v) for v in keep if isinstance(v, int)]
    if nulls:
        nulls += [str(v) for v in nulls if isinstance(v, int)]
    if mapping:
        for k in list(mapping.keys()):
            if isinstance(k, int):
                mapping[str(k)] = mapping[k]

    def map_val(val):
        if pd.isna(val) or val == " ":
            return pd.NA
        if nulls is not None and val in nulls:
            return pd.NA
        elif keep is not None:
            if val in keep:
                return type_check(val)
            else:
                return pd.NA
        elif mapping is not None:
            if val in mapping:
                return type_check(mapping[val])
            else:
                return pd.NA
        else:
            return type_check(val)
        
    if isinstance(val_or_series, pd.Series):
        return val_or_series.apply(map_val)
    else:
        return map_val(val_or_series)


## Validate that values were recoded properly
def validate_variable(df_var, validator):
    distinct_values = df_var.dropna().unique()
    if len(distinct_values) == 0:
        raise ValueError("No non-missing values to validate in variable!")
    for val in distinct_values:
        if hasattr(validator, '__iter__') and not isinstance(validator, str):
            if val not in validator:
                raise ValueError(f"Value {val} not in allowed set of {validator}")
        elif callable(validator):
            if not validator(val):
                raise ValueError(f"Value {val} failed validation function")
    return True

## Compute weighted mean
def weighted_mean(data, val_col, weight="weight"):
    #print(type(data))
    nomiss = data[data[val_col].notna() & data[weight].notna()]
    if len(nomiss) == 0:
        raise ValueError("No valid data to compute weighted mean")
    return (nomiss[val_col] * nomiss[weight]).sum() / nomiss[weight].sum()


## Plot a weighted aggregate function of a variable over time, usually weighted mean, optional grouping
def plot_weight_agg_over_time(
    df,
    var,
    weight = "weight",
    time = "year",
    title = None,
    groupby = None,
    agg = weighted_mean,
):
    nomiss = df[df[var].notna() & df[weight].notna()]
    if groupby is not None:
        for g in groupby:
            nomiss = nomiss[nomiss[g].notna()]
    if len(nomiss) == 0:
        raise ValueError("No valid data to plot")
    
    if groupby is not None:
        nomiss.groupby([time] + groupby).apply(agg, var, weight=weight).unstack().plot()
    else:
        nomiss.groupby(time).apply(agg, var, weight=weight).plot()

    if title is None:
        title = f"Average {var} by {time}"
    plt.title(title)
    plt.xticks(df[time].unique())
    plt.show()