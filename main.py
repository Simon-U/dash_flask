
import pandas as pd
import numpy as np
from pathlib import Path

weights = {
    'Technologie Readiness Level': 5,
    'verwendeter Kraftstoff': 6,
    'behandelte Rauchgasmenge': 7,
    'CO2 Rauchgaskonzentration': 3,
    'Anlage Eingangsdruck': 4,
    'Eingangs Prozesstemperatur': 5,
    'CO2 Reinheit': 3,
    'CO2 Abscheiderate': 7,
    'CO2 Temperatur vor Speicherung': 4,
    'Energiebedarf elektrisch': 9,
    'Energiebedarf thermisch': 7,
    'Prozessmittelverbrauch': 3,
    'Abgasvorbehandlung': 10,
    'Platzbedarf': 7
}

dataroot = Path('data')
filename = '01_aussichtsreichsteTechnologien.xlsx'

filepath = dataroot / filename

data = pd.read_excel(filepath, sheet_name='data', index_col=0)
bounds = pd.read_excel(filepath, sheet_name='bounds', index_col=0)

baseparams = data.loc['Vorgabe']
data = data.drop('Vorgabe')

result_df = pd.Series(weights, name='weights')
scores = {}

technologies = data.index
for technology in technologies:  # technology = " DerisCO2"
    scores.update({technology: {}})
    for criterion in bounds.index:  # criterion = "behandelte Rauchgasmenge"
        print(f'tech: {technology}, crit: {criterion}')
        rule = bounds.loc[criterion]['rule']
        series = bounds.loc[criterion]
        series = series.drop('rule')
        value = data.loc[technology][criterion]
        if type(value) == pd.core.series.Series:
            value = value.values[0]
        if type(value) != str:
            if np.isnan(value):
                scores[technology].update({criterion: np.nan})
        if criterion not in scores[technology]:
            if rule == '>=':
                scores[technology].update({criterion: int(series[series < value].tail(1).index[0][-1])})
            elif rule == '==':
                if criterion == 'Abgasvorbehandlung':
                    if value == 'keine':
                        scores[technology].update({criterion: 0})
                    else:
                        full_text = 'WPSN'
                        scores[technology].update({criterion: 4 - np.sum([full_text.count(c) for c in value])})
                elif criterion == 'verwendeter Kraftstoff':
                    scores[technology].update({criterion: int(series[series == value].tail(1).index[0][-1])})
            elif rule == '<=':
                scores[technology].update({criterion: int(series[series > value].tail(1).index[0][-1])})
            elif rule == 'abs(x-x0)/x0 <=':
                value_ = np.abs((value - baseparams[criterion]) / baseparams[criterion])
                scores[technology].update({criterion: int(series[series > value_].tail(1).index[0][-1])})
scores_df = pd.DataFrame(scores)
result_df = pd.merge(left=result_df, right=scores_df, left_index=True, right_index=True)

for technology in technologies:
    # get weights only for those technologies where data exists
    nan_scores = result_df.index[np.isnan(result_df[technology])]
    weights_sum = result_df['weights'].drop(nan_scores).sum()
    result_df[technology] = result_df['weights'] * result_df[technology] / weights_sum

result_df = result_df.drop('weights', axis=1)
result_df.sum()
pass