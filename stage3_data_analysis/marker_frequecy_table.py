import pandas as pd


def valid_sum(file_name):
    df = pd.read_csv(file_name)
    '''marker_frequency = df.groupby('marker').agg({
        'stance type': lambda x: x.unique()[0] if len(x.unique()) == 1 else 'Multiple',
        'construction type': lambda x: x.unique()[0] if len(x.unique()) == 1 else 'Multiple',
    })'''
    ser = df.groupby('marker')['IsStance'].sum()
    table = pd.Series(ser).reset_index()
    table.columns = ['marker', 'IsStance']
    # table = pd.merge(marker_frequency, sum_per_marker, on='marker').sort_values(by='IsStance', ascending=False)
    table = table[table['IsStance'] > 0]

    marker_path = '/Users/caotony/PycharmProjects/csg_thesis/stage2_data_processing/valid_marker.csv'
    df_m = pd.read_csv(marker_path)
    df_m = df_m.rename(columns={'Marker': 'marker'})

    merged_df = pd.merge(table, df_m, on='marker', how='left')
    merged_df = merged_df[['marker', 'Stance Type', 'Construction Type', 'IsStance']]
    merged_df = merged_df.dropna()
    merged_df = merged_df.rename(columns={'Stance Type': 'stance type', 'Construction Type': 'construction type'})
    merged_df.to_csv('fre_' + str(file_name[:4]) + '.csv', index=False)


wait_list = [str(year) + '_check.csv' for year in range(2021, 2024)]
for file in wait_list:
    valid_sum(file)
