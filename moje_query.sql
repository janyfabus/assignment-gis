-- vytvorenie indexov
CREATE INDEX planet_osm_line_gis
ON planet_osm_line
USING GIST (way);

CREATE INDEX planet_osm_polygon_gis
ON planet_osm_polygon
USING GIST (way);

CREATE INDEX planet_osm_point_gis
ON planet_osm_point
USING GIST (way);

CREATE INDEX planet_osm_point_amenity 
ON planet_osm_point (amenity)
	
-- Vsetky puby a restauracie
SELECT row_to_json(fc) FROM 
	( SELECT 'FeatureCollection' As type, 
	    array_to_json(array_agg(f)) As features 
		FROM (SELECT 'Feature' As type , 
			  ST_AsGeoJSON(ST_Transform(way, 4326))::json As geometry, 
			  row_to_json((osm_id, name, "addr:housename","addr:housenumber", amenity)) As properties 
					FROM planet_osm_point 
					where amenity like 'restaurant' or amenity like 'pub' 
			 )As f 
	) As fc;
			  
-- Najdenie 10 najblizsich pubov a restauracii
SELECT row_to_json(fc) FROM 
	( SELECT 'FeatureCollection' AS type, 
		array_to_json(array_agg(f)) AS features 
		FROM (SELECT 'Feature' AS type, 
			ST_AsGeoJSON(ST_Transform(way, 4326))::json AS geometry,
			row_to_json((osm_id, name, "addr:housename","addr:housenumber", amenity)) As properties
			FROM planet_osm_point  
			WHERE amenity LIKE 'restaurant' OR amenity LIKE 'pub' 
				AND ST_Distance_Sphere(ST_Transform(way, 4326), ST_MakePoint(18.0339, 48.8944)) <= 10000
				ORDER BY ST_Distance_Sphere(ST_Transform(way, 4326), ST_MakePoint(18.0339, 48.8944)) ASC
				LIMIT 10
		) AS f
	) AS fc;
																		 
-- Najdenie pubov v oblasti 10 km
SELECT row_to_json(fc) FROM 
	( SELECT 'FeatureCollection' AS type, 
		array_to_json(array_agg(f)) AS features 
		FROM (SELECT 'Feature' AS type, 
			ST_AsGeoJSON(ST_Transform(way, 4326))::json AS geometry,
			row_to_json((osm_id, name, "addr:housename","addr:housenumber", amenity)) As properties
			FROM planet_osm_point  
			WHERE amenity LIKE 'pub' 
				AND ST_Distance_Sphere(ST_Transform(way, 4326), ST_MakePoint(18.0339, 48.8944)) <= 10000
		) AS f
	) AS fc;
									  								  
-- Najdenie restauracii v oblasti 10 km
SELECT row_to_json(fc) FROM 
	( SELECT 'FeatureCollection' AS type, 
		array_to_json(array_agg(f)) AS features 
		FROM (SELECT 'Feature' AS type, 
			ST_AsGeoJSON(ST_Transform(way, 4326))::json AS geometry,
			row_to_json((osm_id, name, "addr:housename","addr:housenumber", amenity)) As properties
			FROM planet_osm_point  
			WHERE amenity LIKE 'restaurant' 
				AND ST_Distance_Sphere(ST_Transform(way, 4326), ST_MakePoint(18.0339, 48.8944)) <= 10000
		) AS f
	) AS fc;
																			 
									
-- najdi 10 najblizsich parkovacich miest od aktualnej polohy
SELECT ST_Area(ST_Transform(way, 4326)::geography) AS area,
	   name, access , ST_AsGeoJSON(ST_Transform(way, 4326)) AS coordinates, 
	   ST_AsGeoJSON(ST_Centroid(ST_Transform(way, 4326))) AS middlepoint,
											 name
FROM planet_osm_polygon 
WHERE amenity = 'parking'
ORDER BY ST_Transform(way, 4326) <-> ST_GeomFromText('POINT(18.0339 48.8944)', 4326)::geography 
LIMIT 10
									 
SELECT ST_AsGeoJSON(ST_Transform(way, 4326)) AS coordinates
FROM planet_osm_polygon 
WHERE amenity = 'parking'
ORDER BY ST_Transform(way, 4326) <-> ST_GeomFromText('POINT(18.0339 48.8944)', 4326)::geography 
LIMIT 10
										 
SELECT row_to_json(fc) FROM 
	( SELECT 'FeatureCollection' AS type, 
		array_to_json(array_agg(f)) AS features 
		FROM (SELECT 'Feature' AS type, 
			ST_AsGeoJSON(ST_Transform(way, 4326))::json AS geometry,
			row_to_json((ST_Area(ST_Transform(way, 4326)::geography), name, access)) As properties
			FROM planet_osm_polygon  
			WHERE amenity = 'parking'
			ORDER BY ST_Transform(way, 4326) <-> ST_GeomFromText('POINT(18.0339 48.8944)', 4326)::geography 
			LIMIT 10
		) AS f
	) AS fc;


-- Ciary, ktore prepajaju bary

SELECT DISTINCT ST_Transform(line.way, 4326) AS line_way, line.highway 
FROM planet_osm_polygon AS polygon 
cross JOIN planet_osm_line AS line 
WHERE polygon.amenity = 'pub' AND ST_Intersects(polygon.way, line.way) 
AND line.highway 
IN ('sidewalk', 'path', 'footway', 'bridleway', 'steps', 'pedestrian', 'living_street') 

SELECT DISTINCT ST_Transform(line.way, 4326) AS line_way, line.highway 
FROM planet_osm_polygon AS polygon 
cross JOIN planet_osm_line AS line 
WHERE polygon.amenity = 'pub'  
AND line.highway 
IN ('sidewalk', 'path', 'footway', 'bridleway', 'steps', 'pedestrian', 'living_street') 		  
			
			  