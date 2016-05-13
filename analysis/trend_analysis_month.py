
# coding: utf-8

import pandas as pd, numpy as np, geopandas as gpd
import datetime
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("white", {'ytick.major.size': 10.0})
sns.set_context("poster", font_scale=1.1)

def convertTime(dt):
    d = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    d = d.replace(day=1, hour=0)
    return d

def convertCount(ct):
    c = np.int64(np.float64(ct))
    return c

trips = pd.read_csv('../data/aggregated/merged.csv', converters={'datetime': convertTime, 'u_count': convertCount})
trips_agg = trips.groupby(['zone', 'datetime'], as_index=False).agg({'m_count': np.sum, 'u_count': np.sum})

no_pickup_zones = list(set(trips_agg[(trips_agg['m_count']==0) & (trips_agg['u_count']==0)]['zone'].values))

for z in no_pickup_zones:
    trips_agg = trips_agg[trips_agg['zone']!=z]
trips_agg = trips_agg.reset_index(drop=True)
trips_agg['total'] = (trips_agg['m_count']+trips_agg['u_count']).astype(np.float64)
trips_agg['m_percent'] = 100*trips_agg['m_count']/trips_agg['total']
trips_agg['u_percent'] = 100*trips_agg['u_count']/trips_agg['total']
trips_agg = trips_agg.drop('total', axis=1)

corr_list = []
for z in trips_agg.zone.unique():
    corr, p_val = pearsonr(trips_agg[trips_agg['zone']==z]['m_count'].values, trips_agg[trips_agg['zone']==z]['u_count'].values)
    corr_list.append((z,corr,p_val))

plt.figure()
plt.title('Correlation Histogram between Medallion and Uber Pickups in all Taxi Zones by Months')
plt.hist([i[1] for i in corr_list])
plt.savefig('../plots/correlation_histogram.png')

zones = gpd.read_file('../data/geo/taxi_zones.geojson')
corr_by_zones = pd.DataFrame(corr_list, columns=['zone', 'corr_by_mon', 'p_val']).drop('p_val', axis=1)
corr_by_zones = pd.merge(zones, corr_by_zones, on='zone')
corr_by_zones.to_csv('../data/geo/correlation_by_zones.csv', index=False)
