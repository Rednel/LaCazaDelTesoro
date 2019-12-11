/**
 * Please include the following scripts in order to make this
 * libary work:
 *  <script src='https://api.mapbox.com/mapbox-gl-js/v1.4.1/mapbox-gl.js'></script>
 *  <script src='https://api.tiles.mapbox.com/mapbox.js/plugins/turf/v3.0.11/turf.min.js'></script>
 *  <script src='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.0.9/mapbox-gl-draw.js'></script>
 *  <script src='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.4.2/mapbox-gl-geocoder.min.js'></script>
 *  <link rel='stylesheet' href='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.4.2/mapbox-gl-geocoder.css' type='text/css' />
 *  <link rel='stylesheet' href='https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.0.9/mapbox-gl-draw.css' type='text/css'/>
 *  <link href='https://api.mapbox.com/mapbox-gl-js/v1.4.1/mapbox-gl.css' rel='stylesheet' />
 *
 *  Create an interactive map:
 *    - Create an html div with an identifier in your HTML as the followinf examples:
 *        `<div id='your-id' style='width: 800px; height: 800px;'></div>`
 *    - Initialice the component in your own javascript:
 *        createInteractiveMap('your-id');
 */

/**
 * Generates global references
 */
var maps = new Object();
var drawers = new Object();

/**
 * Set the current user location into the rendered map
 * @param {*} map
 */
function setLocation(map) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      map.setCenter([position.coords.longitude, position.coords.latitude]);
    });
  }
}

/**
 * Export the map which correspond with the given identifier
 * @param {*} id
 */
function exportMap(id) {
  return JSON.stringify(drawers[id].getAll());
}

/**
 * Close the create treasure popup
 * @param {*} id
 * @param {*} coordinates
 */
function closePopup(id, coordinates) {
  var popup = document.querySelector('.mapboxgl-popup-content');
  if (id) {
    deleteMarker(id, coordinates);
  }
  popup.style.display = "none";
}

/**
 * Set the marker with the given coordinates into the map with
 * the given identifier
 * @param {*} id
 * @param {*} coordinates
 */
function setMarker(id, coordinates) {
  map = maps[id];
  var errorElement = document.querySelector('.treasure-error');
  try {
    var name = document.querySelector('#treasure-input').value;
    if (name === "") {
      throw new RangeError("empty name");
    }
    map.addSource(name, convertToGeoJSON(coordinates));
    setPointName(id, coordinates, name);
    createMarkerElement(id, coordinates, name);
    closePopup();
  }
  catch (err) {
    if (err instanceof RangeError) {
      document.getElementById("treasure-error-msg").innerHTML = "Empty name";
    }
    errorElement.style.display = "block";
  }
}

/**
 * Creates a marker icon element into the given coordinates which
 * contains the name
 * @param {*} id
 * @param {*} coordinates
 * @param {*} name
 */
function createMarkerElement(id, coordinates, name) {
  map = maps[id];
  marker_id = `marker-${name}`;
  popup_id = `popup-marker-${name}`;
  var popup = new mapboxgl.Popup({ closeOnClick: true })
  .setLngLat(coordinates)
  .setHTML(`
  <div class="treasure-info" id="${popup_id}">
    <p class="treasure-name">${name}</p>
    <div class="treasure-buttons">
      <a class="waves-effect waves-light osm-outline-sm-red" onclick="deleteFullMarker('${id}', '${marker_id}', '${popup_id}', '${coordinates}')">Delete</a>
    </div>
  </div>
`);
  var marker = document.createElement('div');
  marker.setAttribute('id', marker_id);
  marker.className = 'marker';
  marker.style.backgroundImage = 'url("../static/img/marker.svg")';
  marker.style.width = '40px';
  marker.style.height = '40px';

  marker.addEventListener('mouseover', function () {
    popup.addTo(map);
  });

  new mapboxgl.Marker(marker)
  .setLngLat(coordinates)
  .addTo(map);
}

/**
 * Removes a marker from the map which correspond with the given
 * identifier
 * @param {*} id
 * @param {*} marker_id
 * @param {*} popup_id
 * @param {*} coordinates
 */
function deleteFullMarker(id, marker_id, popup_id, coordinates) {
  document.getElementById(marker_id).remove();
  document.getElementById(popup_id).parentElement.remove();
  this.deleteMarker(id, coordinates);
}

/**
 * Delete the marker
 * @param {*} id
 * @param {*} coordinates
 */
function deleteMarker(id, coordinates) {
  drawer = drawers[id];
  var feature_id = searchFeature(drawer.getAll().features, coordinates);
  drawer.delete(feature_id);
}

/**
 * Add name property to the current geoJSON
 * @param {*} id
 * @param {*} coordinates
 * @param {*} name
 */
function setPointName(id, coordinates, name) {
  var drawer = drawers[id];
  var feature_id = searchFeature(drawer.getAll().features, coordinates);
  drawer.setFeatureProperty(feature_id, 'name', name);
}

/**
 * Search feature into the drawer
 * @param {*} features
 * @param {*} coordinates
 */
function searchFeature(features, coordinates) {
  var feature_id;
  features.map((feature) => {
    if (feature.geometry.coordinates.every(e => coordinates.includes(e))) {
      feature_id = feature.id;
    };
  });
  return feature_id;
}

/**
 * Convert coordinates into geoJSON format
 * @param {*} coordinates
 */
function convertToGeoJSON(coordinates) {
  return {
    type: "geojson",
    data: {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: {},
          geometry: {
            type: "Point",
            coordinates: coordinates
          }
        }
      ]
    }
  };
}

/**
 * Render the given geoJSON into the div with the given identifier
 * @param {*} id
 * @param {*} geojson
 */
function renderGeoJSON(id, geojson) {
  mapboxgl.accessToken =
    "pk.eyJ1IjoiYWx2YXJvZ2Y5NyIsImEiOiJjazMzMG1qdGMwYjMzM25tcTNtNmN5c2RqIn0.pXXfUb1xKca_E8NLPVnyLw";

  var map = new mapboxgl.Map({
    container: id,
    style: "mapbox://styles/mapbox/streets-v11",
    center: [0, 0],
    zoom: 12
  });
  var draw = new MapboxDraw();
  maps[id] = map;
  drawers[id] = draw;

  var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    marker: {
      color: "orange"
    },
    mapboxgl: mapboxgl
  });

  map.addControl(geocoder);
  map.addControl(draw);
  setLocation(map);
  geojson_data = JSON.parse(geojson);
  draw.set(geojson_data);
  geojson_data.features.map(feature => {
    if(feature.geometry.type === "Point"){
      createMarkerElement(id, feature.geometry.coordinates, feature.properties.name)
    }
  })
  document.querySelector(`#${id}`).querySelector('.mapboxgl-ctrl-geocoder--input').classList.toggle('browser-default');
}

/**
 * Creates an interactive map into the container with the
 * given identifier
 * @param {*} id
 */
function createInteractiveMap(id) {
  mapboxgl.accessToken =
    "pk.eyJ1IjoiYWx2YXJvZ2Y5NyIsImEiOiJjazMzMG1qdGMwYjMzM25tcTNtNmN5c2RqIn0.pXXfUb1xKca_E8NLPVnyLw";

  var markerActive = false;
  var map = new mapboxgl.Map({
    container: id,
    style: "mapbox://styles/mapbox/streets-v11",
    center: [0, 0],
    zoom: 12
  });
  maps[id] = map;

  var draw = new MapboxDraw();
  drawers[id] = draw;

  var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    marker: {
      image: "../static/img/marker.svg",
      color: "orange"
    },
    mapboxgl: mapboxgl
  });

  map.addControl(geocoder);
  map.addControl(new mapboxgl.NavigationControl());
  map.addControl(draw);

  var pointElement = document.querySelector('.mapbox-gl-draw_point')
  pointElement.addEventListener('click', function () {
    markerActive = true;
  })

  map.on("click", function (e) {

    if (markerActive) {
      coordinates = [e.lngLat.lng, e.lngLat.lat];
      new mapboxgl.Popup({ closeOnClick: true })
      .setLngLat(coordinates)
      .setHTML(`
        <div class="treasure-input">
          <div class="treasure-form">
            <div class="input-field">
              <input id="treasure-input" type="text">
              <label for="treasure-input">Treasure Name</label>
            </div>
          </div>
          <div class="treasure-error">
            <p id="treasure-error-msg">Name already set, please change it!</p>
          </div>
          <div class="treasure-buttons">
            <a class="waves-effect waves-light osm-outline-sm" onclick="setMarker('${id}', coordinates)">Create</a>
            <a class="waves-effect waves-light osm-outline-sm-red" onclick="closePopup('${id}', coordinates)">Cancel</a>
          </div>
        </div>
      `)
      .addTo(map);
    }
    markerActive = false;
  });

  setLocation(map);
  document.querySelector(`#${id}`).querySelector('.mapboxgl-ctrl-geocoder--input').classList.toggle('browser-default');
}