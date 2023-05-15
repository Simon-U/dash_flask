import pandas as pd
import numpy as np
from pathlib import Path



def get_data(file_path, weights):
    data = pd.read_excel(file_path, sheet_name="data", index_col=0)
    bounds = pd.read_excel(file_path, sheet_name="bounds", index_col=0)

    baseparams = data.loc["Vorgabe"]
    data = data.drop("Vorgabe")

    result_df = pd.Series(weights, name="weights")
    result_df.index = bounds.index.copy()
    scores = {}

    technologies = data.index
    for technology in technologies:  # technology = " DerisCO2"
        scores.update({technology: {}})
        for criterion in bounds.index:  # criterion = "behandelte Rauchgasmenge"
            # print(f"tech: {technology}, crit: {criterion}")
            rule = bounds.loc[criterion]["rule"]
            series = bounds.loc[criterion]
            series = series.drop("rule")
            value = data.loc[technology][criterion]
            if type(value) == pd.core.series.Series:
                value = value.values[0]
            if type(value) != str:
                if np.isnan(value):
                    scores[technology].update({criterion: np.nan})
            if criterion not in scores[technology]:
                if rule == ">=":
                    scores[technology].update(
                        {criterion: int(series[series < value].tail(1).index[0][-1])}
                    )
                elif rule == "==":
                    if criterion == "Abgasvorbehandlung":
                        if value == "keine":
                            scores[technology].update({criterion: 0})
                        else:
                            full_text = "WPSN"
                            scores[technology].update(
                                {
                                    criterion: 4
                                    - np.sum([full_text.count(c) for c in value])
                                }
                            )
                    elif criterion == "verwendeter Kraftstoff":
                        if value in ['Methanol', 'LNG', 'MGO', 'HFO']:
                            scores[technology].update(
                                {
                                    criterion: int(
                                        series[series == value].tail(1).index[0][-1]
                                    )
                                }
                            )
                        else:
                            scores[technology].update(
                                {
                                    criterion: 0
                                }
                            )
                elif rule == "<=":
                    scores[technology].update(
                        {criterion: int(series[series > value].tail(1).index[0][-1])}
                    )
                elif rule == "abs(x-x0)/x0 <=":
                    value_ = np.abs(
                        (value - baseparams[criterion]) / baseparams[criterion]
                    )
                    scores[technology].update(
                        {criterion: int(series[series > value_].tail(1).index[0][-1])}
                    )
    scores_df = pd.DataFrame(scores)
    result_df = pd.merge(
        left=result_df, right=scores_df, left_index=True, right_index=True
    )
    # Fill not available technology scores with 0
    result_df = result_df.fillna(0)
    for technology in technologies:
        weights_sum = result_df["weights"].sum()
        result_df[technology] = (result_df["weights"] * result_df[technology] / weights_sum)

    result_df = result_df.drop("weights", axis=1)

    technologies_score = result_df.sum()
    technologies_score = technologies_score.sort_values(ascending=False)

    result_sorted = pd.DataFrame(index=result_df.index)
    for tx in technologies_score.index:
        result_sorted[tx] = result_df[tx]

    return result_sorted, technologies_score
