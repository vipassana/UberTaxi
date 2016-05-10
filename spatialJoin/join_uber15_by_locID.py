__author__="Shi Fan"
import numpy as np
import pandas as pd
import csv
from glob import glob
from datetime import datetime

if __name__=="__main__":
	lookup = pd.read_csv('../data/uber/taxi-zone-lookup.csv')

	uber15trips = []

	for data in glob('../data/uber/*15*/part*'):
		with open(data, 'rb') as f:
			csv_reader = csv.reader(f)
			uber15trips.extend([(datetime.strptime(record[0][:-2], '%Y-%m-%d %H:%M:%S'), np.int64(record[1])) for record in csv_reader])

	trips = pd.DataFrame(uber15trips, columns=['PickupTime', 'LocationID'])

	trips_merged = pd.merge(trips, lookup, on='LocationID')

	trips_merged.to_csv('../data/preprocessed/uber_janjun15.csv', index=False)