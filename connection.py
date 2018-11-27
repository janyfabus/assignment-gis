import random
import string
import os, os.path
import cherrypy
import csv
import psycopg2
import json

conn = psycopg2.connect(database="PDT_projekt", user = "postgres", password = "janulka", host = "127.0.0.1", port = "5432")
print ("Opened database successfully")
cur = conn.cursor()

class AppGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

class AllDataWebservice(object):
    exposed = True
    def GET(self, **params):
        print("Parametre", params)
        # print("search name", search_name)
        # filtrovany atribut
        search_name = params['search_name'] 
        print("aaaaaaaaaaaaaa", search_name)
        # ak mam k dispo meno filtrujem inak vsetko
        if (search_name != ''):
            cur.execute(
                "SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type , ST_AsGeoJSON(ST_Transform(way, 4326))::json As geometry, row_to_json((osm_id,name,"'"addr:housename"'","'"addr:housenumber"'",amenity)) As properties FROM planet_osm_point where (amenity like 'restaurant' or amenity like 'pub') and name like %s ) As f )  As fc; ", [search_name]
            )
        else:
            cur.execute(
                "SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type , ST_AsGeoJSON(ST_Transform(way, 4326))::json As geometry, row_to_json((osm_id,name,"'"addr:housename"'","'"addr:housenumber"'",amenity)) As properties FROM planet_osm_point where amenity like 'restaurant' or amenity like 'pub' ) As f )  As fc; "
            )
        first = True
        for zaznam in cur:
            if first == True:
                result_json = json.dumps(zaznam)
                first = False
            else:
                result_json = result_json.concat(json.dumps(zaznam))
        print("Vysledny JSON: ", result_json)
        return result_json

class PubsWebService(object):
    exposed = True
    def GET(self):
        #  vsetky puby
        cur.execute(
            "SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type , ST_AsGeoJSON(ST_Transform(way, 4326))::json As geometry, row_to_json((osm_id,name,"'"addr:housename"'","'"addr:housenumber"'",amenity)) As properties FROM planet_osm_point where amenity like 'pub'   ) As f )  As fc; "
        )
        first = True
        for zaznam in cur:
            if first == True:
                result_json = json.dumps(zaznam)
                first = False
            else:
                result_json = result_json.concat(json.dumps(zaznam))
        print("Vysledny JSON pubs: ", result_json)
        return result_json

class RestaurantWebService(object):
    exposed = True
    def GET(self):
        #  vsetky restauracie
        cur.execute(
            "SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type , ST_AsGeoJSON(ST_Transform(way, 4326))::json As geometry, row_to_json((osm_id,name,"'"addr:housename"'","'"addr:housenumber"'",amenity)) As properties FROM planet_osm_point where amenity like 'restaurant'  ) As f )  As fc; "
        )
        first = True
        for zaznam in cur:
            if first == True:
                result_json = json.dumps(zaznam)
                first = False
            else:
                result_json = result_json.concat(json.dumps(zaznam))
        print("Vysledny JSON restaurant: ", result_json)
        return result_json

class Distance10(object):
    exposed = True
    def GET(self):
        #  10 najblizsich
        cur.execute(
            "SELECT row_to_json(fc) FROM( SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) AS features FROM (SELECT 'Feature' AS type, ST_AsGeoJSON(ST_Transform(way, 4326))::json AS geometry,row_to_json((osm_id, name, "'"addr:housename"'","'"addr:housenumber"'", amenity)) As properties FROM planet_osm_point WHERE amenity LIKE 'restaurant' OR amenity LIKE 'pub' AND ST_Distance_Sphere(ST_Transform(way, 4326), ST_MakePoint(18.0339, 48.8944)) <= 5000 ORDER BY ST_Distance_Sphere(ST_Transform(way, 4326), ST_MakePoint(18.0339, 48.8944)) ASC LIMIT 10) AS f) AS fc; "
        )
        first = True
        for zaznam in cur:
            if first == True:
                result_json = json.dumps(zaznam)
                first = False
            else:
                result_json = result_json.concat(json.dumps(zaznam))
        print("Vysledny JSON 10: ", result_json)
        return result_json

class ParkingPlaces(object):
    exposed = True
    def GET(self):
        #  najblizsie parkoviska v mojom okoli
        cur.execute(
            "SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' AS type, array_to_json(array_agg(f)) AS features FROM (SELECT 'Feature' AS type, ST_AsGeoJSON(ST_Transform(way, 4326))::json AS geometry, row_to_json((ST_Area(ST_Transform(way, 4326)::geography), name, access)) As properties FROM planet_osm_polygon WHERE amenity = 'parking' ORDER BY ST_Transform(way, 4326) <-> ST_GeomFromText('POINT(18.0339 48.8944)', 4326)::geography LIMIT 20 ) AS f ) AS fc;"
        )
        first = True
        for zaznam in cur:
            if first == True:
                result_json = json.dumps(zaznam)
                first = False
            else:
                result_json = result_json.concat(json.dumps(zaznam))
        print("PARKOVISKA: ", result_json)
        return result_json

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/alldata': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/pubs': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/restaurant': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        '/distance': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/parking': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    webapp = AppGenerator()
    webapp.alldata = AllDataWebservice()
    webapp.pubs = PubsWebService()
    webapp.restaurant = RestaurantWebService()
    webapp.distance = Distance10()
    webapp.parking = ParkingPlaces()
    cherrypy.quickstart(webapp, '/', conf)
