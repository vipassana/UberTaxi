
# coding: utf-8

import pandas as pd, numpy as np
import datetime
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('fivethirtyeight')
sns.set_style("white", {'ytick.major.size': 10.0})
sns.set_context("poster", font_scale=1.1)

corr_by_month = pd.read_csv('../data/geo/correlation_by_zones.csv')
red_zones = corr_by_month[corr_by_month.corr_by_mon<=-0.690940643947]['zone'].values

def convertTime(dt):
    d = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    d = d.replace(day=1)
    return d

def convertCount(ct):
    c = np.int64(np.float64(ct))
    return c

trips = pd.read_csv('../data/aggregated/merged.csv',                     converters={'datetime': convertTime, 'u_count': convertCount})
trips_agg = trips.groupby(['zone', 'datetime'], as_index=False).agg({'m_count': np.sum, 'u_count': np.sum})

for z in trips_agg.zone.unique():
    if z not in red_zones:
        trips_agg = trips_agg[trips_agg['zone']!=z]
print len(trips_agg)

trips_agg = trips_agg.reset_index(drop=True)
trips_agg['total'] = (trips_agg['m_count']+trips_agg['u_count']).astype(np.float64)
trips_agg['m_percent'] = 100*trips_agg['m_count']/trips_agg['total']
trips_agg['u_percent'] = 100*trips_agg['u_count']/trips_agg['total']
trips_agg = trips_agg.drop('total', axis=1)
trips_agg['hour'] = trips_agg['datetime'].apply(lambda x: x.hour)

x = np.arange(12)
A = np.vstack([x, np.ones(len(x))]).T

hour_dict = {}
for z in trips_agg.zone.unique():
    hour_dict[z] = []
    for h in np.arange(24):
        u_array = trips_agg[(trips_agg.zone==z) & (trips_agg.hour==h)]['u_percent'].values
        slope, intercept = np.linalg.lstsq(A, u_array)[0]
        hour_dict[z].append(slope)

list_for_hist = []
for zone,arr in hour_dict.iteritems():
    list_for_hist.append(np.argmax(np.array(arr)))

plt.figure()
plt.title('Histogram of Fastest-growing Uber Pickup Percentage in "Red Zones" by Hours')
plt.hist(list_for_hist, bins=range(min(list_for_hist), max(list_for_hist) + 2, 1))
plt.xlim(-.5,24.5)
plt.ylim(0,8.25)
plt.show()

