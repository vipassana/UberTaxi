import pandas as pd, numpy as np

uber = pd.read_csv('../data/aggregated/uber14_agg_final.csv')
uber15 = pd.read_csv('../data/aggregated/uber15_agg_final.csv')
uber = uber.append(uber15, ignore_index=True)
uber = uber.sort(['borough', 'zone', 'datetime'])
uber = uber.reset_index(drop=True)
uber.to_csv('../data/aggregated/uber_agg_final.csv', index=False)