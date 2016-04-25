#!/usr/bin/python

__author__="Shi Fan"
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from datetime import datetime

sqlContext = SQLContext(sc)
trips = sc.textFile("uber_data/*15.csv")
header = trips.first()
schemaString = header
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split(",")]
tripsNoHeader = trips.filter(lambda l: "Dispatching_base_num" not in l)
tripsClean = tripsNoHeader.filter(lambda l: l!="")
fields[1].dataType = TimestampType()
fields[-1].dataType = IntegerType()
sel_fields = [fields[i] for i in [1, -1]]
schema = StructType(sel_fields)
trips_temp = tripsClean.map(lambda k: k.split(",")).map(lambda p: (datetime.strptime(p[1], "%Y-%m-%d %H:%M:%S"), int(p[-1])))
trips_df = sqlContext.createDataFrame(trips_temp, schema)
trips_df.write.format("com.databricks.spark.csv").save("uber_15_output")