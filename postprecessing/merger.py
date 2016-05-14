import pandas as pd, numpy as np

medallion = pd.read_csv('../data/aggregated/medallion_agg_final.csv')
uber = pd.read_csv('../data/aggregated/uber14_agg_final.csv')
uber15 = pd.read_csv('../data/aggregated/uber15_agg_final.csv')
uber = uber.append(uber15, ignore_index=True)
uber = uber.sort(['borough', 'zone', 'datetime'])
uber = uber.reset_index(drop=True)
merged = medallion.copy()
merged = merged.rename(columns={'count': 'm_count'})
merged['u_count'] = uber['count']
merged.to_csv('../data/aggregated/merged.csv', index=False)