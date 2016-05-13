#!/usr/bin/python

from pyspark import SparkContext
import datetime

def indexZones(geojsonFile):
    from rtree import index
    import geopandas as gpd
    import fiona.crs
    zones = gpd.read_file(geojsonFile).to_crs(fiona.crs.from_epsg(2263))
    idx = index.Index()

    for cnt,geometry in enumerate(zones.geometry):
        idx.insert(cnt, geometry.bounds)

    return (idx, zones)

def findZone(p, index, zones):
    match = index.intersection((p.x, p.y, p.x, p.y))
    for idx in match:
        if any(map(lambda x: x.contains(p), zones.geometry[idx])):
            return idx
    return -1

def mapToZone(trips):
    import pyproj
    import shapely.geometry as geom
    proj = pyproj.Proj(init="epsg:2263", preserve_units=True)
    index, zones = indexZones('taxi_zones.geojson')

    for trip in trips:
        p = trip.strip().split(',')
        t = datetime.datetime.strptime(p[0][:-2], "%Y-%m-%d %H:%M:%S").replace(second=0, minute=0)
        pickup_loc  = geom.Point(proj(float(p[1]), float(p[2])))
        pickup_zone = findZone(pickup_loc, index, zones)
        if pickup_zone>=0:
        	yield (str(zones.borough[pickup_zone])+','+str(zones.zone[pickup_zone])+','+t.strftime('%Y-%m-%d %H'), 1)

def main():
    sc = SparkContext()
    trips = sc.textFile("YEAR_MONTH_output/part*")
    trips_ = trips.mapPartitions(mapToZone).reduceByKey(lambda a, b: (a+b))
    trips_.saveAsTextFile("medallion_MONTH_YEAR_agg")

if __name__=="__main__":
    main()