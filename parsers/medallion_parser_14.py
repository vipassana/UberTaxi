#!/usr/bin/python

# download data from http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml
# this script parses pickup time, lat, lon, fare, surcharge, and tip for each trip in 2014
# module load python/gnu/2.7.11
# module load spark/1.4.0
# pyspark --packages com.databricks:spark-csv_2.10:1.4.0 --executor-memory 16g --driver-memory 8g
__author__="Shi Fan"
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from datetime import datetime

sqlContext = SQLContext(sc)
trips = sc.textFile("yellow_tripdata_YEAR-MONTH.csv")
header = trips.first()
schemaString = header
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split(", ")]

tripsNoHeader = trips.filter(lambda l: "vendor_id" not in l)
tripsClean = tripsNoHeader.filter(lambda l: l!="")
tripsClean = tripsClean.filter(lambda t: float(t.strip().split(",")[5])!=0)
tripsClean = tripsClean.filter(lambda t: float(t.strip().split(",")[6])!=0)

fields[1].dataType = TimestampType()
fields[5].dataType = FloatType()
fields[6].dataType = FloatType()
fields[-6].dataType = FloatType()
fields[-5].dataType = FloatType()
fields[-3].dataType = FloatType()
sel_fields = [fields[i] for i in [1, 5, 6, -6, -5, -3]]
schema = StructType(sel_fields)

trips_temp = tripsClean.map(lambda k: k.split(",")).map(lambda p: (datetime.strptime(p[1], "%Y-%m-%d %H:%M:%S"),float(p[5]), float(p[6]), float(p[-6]), float(p[-5]), float(p[-3])))
trips_df = sqlContext.createDataFrame(trips_temp, schema)
trips_df.write.format("com.databricks.spark.csv").save("YEAR_MONTH_output")