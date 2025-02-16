import pandas as pd


def valid_sum(file_name):
    df = pd.read_csv(file_name)
    marker_frequency = df.groupby('marker').agg({
        'stance type': lambda x: x.unique()[0] if len(x.unique()) == 1 else 'Multiple',
        'construction type': lambda x: x.unique()[0] if len(x.unique()) == 1 else 'Multiple',
    })
    sum_per_marker = df.groupby('marker')['IsStance'].sum()
    table = pd.merge(marker_frequency, sum_per_marker, on='marker').sort_values(by='IsStance', ascending=False)
    table = table[table['IsStance'] > 0].sort_values(by=['stance type', 'construction type'])
    table.to_csv("marker_fre" + file_name[:4] + '.csv')


wait_list = [str(year) + '_check.csv' for year in range(2021, 2024)]
for file in wait_list:
    valid_sum(file)
