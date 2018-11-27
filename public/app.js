L.mapbox.accessToken = 'pk.eyJ1IjoiamFua2h1bGllbmthIiwiYSI6ImNqbjd0c3QxbjNtZ3IzcHF2dGR5Mm9kYXIifQ.aHjrbeYkaB3M7hrbbHhisw';
var user_long;
var user_lat;
var locations;
var map = L.mapbox.map('map', 'mapbox.streets')
    .setView([48.891132, 18.042297], 12);

// fake locacion
function findMyLocation() {
    map.setView([18.0339, 48.8944], 14);
    locale.openPopup();
    return false;
}

function getPubs() {
    $.getJSON("/pubs", function(result) { 
        console.log(result)
        clearPanel('listings');
        initializeMap(result);
    })
}

function getRestaurant() {
    $.getJSON("/restaurant", function(result) { 
        console.log(result)
        clearPanel('listings');
        initializeMap(result);
    })
}

function getDistance() {
    $.getJSON("/distance", function(result) { 
        console.log(result)
        clearPanel('listings');
        initializeMap(result);
    })
}

function getParking() {
    $.getJSON("/parking", function(result) { 
        console.log(result)
        clearPanel('listings');
        initializeMap(result);
    })
}

function filterByName() {
    var name = $("input[name='search_name']").val();
    console.log("hladane meno", name);
    $.getJSON("/alldata", {"search_name": name}, function(result) { 
        console.log(result)
        clearPanel('listings');
        initializeMap(result);
    })
}

function initializeMap(geojson) {
    if (geojson == null) {
        locations.clearLayers();
    }
    else {
        geojson[0].features = setMarkers(geojson[0].features);

        var listings = document.getElementById("listings");

        if (!locations) {
            locations = L.mapbox.featureLayer().setGeoJSON(geojson).addTo(map);
        } else {
            locations.clearLayers();
            locations.setGeoJSON(geojson);
        }
        console.log(locations);

        function setActive(el) {
            var siblings = listings.getElementsByTagName("div");
            for (var i=0; i<siblings.length; i++) {
                siblings[i].className = siblings[i].className.replace(/active/, '').replace(/\s\s*$/, '');
            }
            el.className += "active";
        }

        locations.eachLayer(function(locale) {
            // Shorten locale.feature.properties to just `prop` so we're not
            // writing this long form over and over again.
            var prop = locale.feature.properties;
            console.log("PROOOOOP", prop);
            // console.log(locale.feature.geometry.coordinates[0]);
        
            if (!prop.name) { 
                // else if (locale.feature.geometry.coordinates[0] == 18.0339 && locale.feature.geometry.coordinates[1] == 48.8944)
                if (prop.title == 'Here I am!')
                {
                    var pub_name = 'Moja poloha';
                } 
                // Each marker on the map.
                else if (prop.f2 == null) 
                {
                    var pub_name = 'Parkovisko';
                }
                else 
                {
                    var pub_name = prop.f2;
                }
                var popup = '<h3>' + pub_name + '</h3><div>Typ podniku: ' + prop.f5;
        
                var listing = listings.appendChild(document.createElement('div'));
                listing.className = 'item';
                var link = listing.appendChild(document.createElement('a'));
                link.href = '#';
                link.className = 'title';
                link.innerHTML = pub_name;
                // var details = listing.appendChild(document.createElement('div'));
                // details.innerHTML = 'Typ podniku: ' + prop.f5;
        
                link.onclick = function() {
                    setActive(listing);
                    // When a menu item is clicked, animate the map to center
                    // its associated locale and open its popup.
                    console.log("toto potrebujem na moju polohu", locale.getLatLng());
                    map.setView(locale.getLatLng(), 14);
                    locale.openPopup();
                    return false;
                };
                // Marker interaction
                locale.on('click', function(e) {
                // 1. center the map on the selected marker.
                map.panTo(locale.getLatLng());
                // 2. Set active the markers associated listing.
                setActive(listing);
                });
                popup += '</div>';
                locale.bindPopup(popup);
            }
        });
    }
    map.fitBounds(locations.getBounds());
}

function clearPanel(elementID) {
    document.getElementById(elementID).innerHTML = "";
}

function setMarkers(features) {
    if (features) {
        for (var i = 0; i < features.length; i++) {
            if (features[i].properties.f5 == 'pub') {
                features[i].properties['marker-symbol'] = 'alcohol-shop';
                features[i].properties['marker-color'] = '#bb86fc';
            } else {
                features[i].properties['marker-symbol'] = 'restaurant';
                features[i].properties['marker-color'] = '#FF6138';
            }
        }
        features[features.length] = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    18.0339, 48.8944
                ]
            },
            "properties": {
                "title": "Here I am!",
                "marker-size": "medium",
                "marker-color": "#3CA0D3",
                "marker-symbol": "pitch"
            }
        };
        return features;
    } else {
        return null;
    }
}
