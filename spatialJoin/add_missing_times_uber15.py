__author__="Shi Fan"
import numpy as np, pandas as pd
import datetime

with open('../data/aggregated/uber15_agg_output/part-00000','rb') as f:
	lines = f.readlines()
f.close()

uber15 = []
for line in lines:
	key, cnt = line.strip().split('\t')
	parts = key.strip().split(',')
	uber15.append((parts[0], parts[1], datetime.datetime.strptime(parts[2], '%Y-%m-%d %H'), np.int64(cnt)))

trips = pd.DataFrame(uber15, columns=['borough', 'zone', 'time', 'count'])

start15 = datetime.datetime.strptime("2015-01-01", "%Y-%m-%d")
end15 = datetime.datetime.strptime("2015-07-01", "%Y-%m-%d")
time15 = [start15 + datetime.timedelta(days=x) + datetime.timedelta(hours=y) for x in range(0, (end15-start15).days) for y in range(0,24)]

trips['datetime'] = trips['time'].apply(lambda x: x.to_datetime())
trips = trips.drop(['time'], axis=1)
trips = trips.reindex(columns=['borough', 'zone', 'datetime', 'count'])

zone_borough_dict = {}
for (z,b) in zip(trips.zone, trips.borough):
	if z not in zone_borough_dict.keys():
		zone_borough_dict[z] = b

times_to_add = []
for z in trips.zone.unique():
	times_missing = list(set(time15)-set(trips[trips.zone==z].datetime.tolist()))
	if len(times_missing)>0:
		for t in times_missing:
			times_to_add.append((zone_borough_dict[z], z, t, 0))

trips_to_add = pd.DataFrame(times_to_add, columns=['borough', 'zone', 'datetime', 'count'])
trips = trips.append(trips_to_add, ignore_index=True)
trips = trips.sort(['borough', 'zone', 'datetime'])
trips = trips.reset_index(drop=True)
trips.to_csv('../data/aggregated/uber15_agg_final.csv', index=False)