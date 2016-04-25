#!/usr/bin/python

__author__="Shi Fan"
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from datetime import datetime

sqlContext = SQLContext(sc)
trips = sc.textFile("uber_data/*14.csv")
header = trips.first()
schemaString = header
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split(",")]
tripsNoHeader = trips.filter(lambda l: "Date/Time" not in l)
tripsClean = tripsNoHeader.filter(lambda l: l!="")
tripsClean = tripsClean.map(lambda l: l.replace('"', ''))
fields[0].dataType = TimestampType()
fields[1].dataType = FloatType()
fields[2].dataType = FloatType()
sel_fields = [fields[i] for i in [0, 1, 2]]
schema = StructType(sel_fields)
trips_temp = tripsClean.map(lambda k: k.split(",")).map(lambda p: (datetime.strptime(p[0], '%m/%d/%Y %H:%M:%S'), float(p[1]), float(p[2])))
trips_df = sqlContext.createDataFrame(trips_temp, schema)
trips_df.write.format("com.databricks.spark.csv").save("uber_14_output")