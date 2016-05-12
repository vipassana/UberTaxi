#!/usr/bin/python

__author__="Shi Fan"
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import datetime
from rtree import index
import geopandas as gpd

sqlContext = SQLContext(sc)
trips = sc.textFile("uber_14_output/part*")
trips_ = trips.map(lambda k: k.split(",")).map(lambda p: (datetime.datetime.strptime(p[0][:-2], "%Y-%m-%d %H:%M:%S").replace(minute=0), float(p[1]), float(p[2]))).cache()
zones = gpd.read_file('../data/taxi_zones.geojson')

start14 = datetime.datetime.strptime("2014-04-01", "%Y-%m-%d")
end14 = datetime.datetime.strptime("2014-10-01", "%Y-%m-%d")
time_idx = [start14 + datetime.timedelta(days=x) + datetime.timedelta(hours=y) for x in range(0, (end14-start14).days) for y in range(0,24)]

tripsList = []
for time in time_idx:
    trips_temp = trips_.filter(lambda t: t[0] == time).cache()
    idx = index.Index()
    for cnt,i in enumerate(trips_temp.collect()):
        idx.insert(cnt,(i[1],i[2],i[1],i[2]))
    for (borough, zone, geometry) in zip(zones.borough, zones.zone, zones.geometry):
        results = list(idx.intersection(geometry.bounds))
        tripsList.append((borough, zone, time, len(results)))

fields = [StructField('borough', StringType(), True), StructField('zone', StringType(), True), StructField('time', TimestampType(), True), StructField('count', IntegerType(), True)]
schema = StructType(fields)
trips_df = sqlContext.createDataFrame(tripsList, schema)
trips_df.write.format("com.databricks.spark.csv").save("uber_aprsep14_agg")