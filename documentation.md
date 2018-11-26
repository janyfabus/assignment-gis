*This is a documentation for a fictional project, just to show you what I expect. Notice a few key properties:*
- *no cover page, really*
- *no copy&pasted assignment text*
- *no code samples*
- *concise, to the point, gets me a quick overview of what was done and how*
- *I don't really care about the document length*
- *I used links where appropriate*

# Úvod
Webová aplikácia zobrazuje reštaurácie a bary v Trenčíne a jeho širšom okolí.
Používateľovi sú umožnené nasledujúce scenáre:
  - zobrazenie reštaurácii
  - zobrazenie barov
  - zobrazenie 1O najbližsích barov/reštaurácií vzhľadom na jeho polohu
  - vykreslenie najbližších parkovísk
  - filtrovanie barov/reštaurácií podľa názvu
  - zobrazenie detailu na klik

Takto to vyzerá v akcii:

![Screenshot](screenshot.png)

Webová aplikácia je zložená z dvoch častí. [Frontend](#frontend), ktorý využíva html, css, mapbox API, mapbox.js a [backend](#backend), ktorý je napísaný v Python-e s použitím frameworku [CherryPy](#http://cherrypy.org) a ďalej komunikuje s PostGIS-om. Frontend a backend komunikujú pomocou RestAPI.

# Frontend

Frontend je staticka HTML stránka, ktorej kód sa nachádza v (`index.html`). Stránka obsahuje mapu a bočný panel. Mapa komunikuje zo serverom prostredníctvom [mapbox.js](https://api.mapbox.com/mapbox.js/v3.1.1/mapbox.js). Všetok potrebný kód sa nachádza v `public/app.js`. Vykonáva sa v ňom komunikácia s backendom, a spracovanie prijatých dát, ktoré prijíma z backendu vo forme JSONu resp geoJSONu. Prijaté dáta zobrazí do mapy a bočného panelu. Tento `geoJSON` sa trocha upravuje, pretože v ňom nie sú informácie o markeroch a tiež poloha používateľa.

# Backend

Backend je napísaný v Pythone pomocou frameworku [CherryPy](#http://cherrypy.org). K databáze sa pripája pomocou `Python` knižnice [psycopg2](http://initd.org/psycopg/). Backend počúva na jednotlivé requesty z [frontendu](#frontend), tieto requesty potom vyhodnocuje a po vykonaní selectu posiela získané dáta naspäť vo formáte `geoJSON`. Všetok kód backendu sa nachádza v `connection.py`.

## Dáta

Dáta sú z Open Street Maps. Stiahnutý je Trenčín a jeho širšie okolie. Tieto dáta boli pomocou osm2pgsql naimportované do databázy. Za účelom zrýchlenia dotazov je vytvorený index na stĺpci amenity, keďže sú z databázy vyberané iba riadky, ktorých amenity je buď "restaurant", alebo "pub". Ďalšie indexy sú vytvorené na stĺpci way v tabuľkách. Geojson je gengerovaný pomocou štandartnej funkcie st_asgeojson a všetky riadky sú spojené priamo v databáze do jedného geojsonu.

## Api



### Response

API vracia gejson, ktorý obsahuje "geometry" a "properties" pre každú nájdenú položku:
```
{
      "type": "Feature", 
      "geometry": {
        "type": "Point", 
        "coordinates": [
          18.0376516, 48.896410799718
        ]
      }, 
      "properties": {
        "f1": 2289661634, 
        "f2": "Na lodenici", 
        "f3": null, 
        "f4": null, 
        "f5": "pub"
      }
  },
```

