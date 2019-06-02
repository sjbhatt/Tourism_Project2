// Path to the JSON map data
var mapdata_url = "http://127.0.0.1:5000/tourism_mapdata.json";

// Marker size function
function markerSize(value) {
  value = Math.pow(value, 0.455) * 5;
  return value;
}

// Color scale function
function colorScale(value) {
  return value >= 15 ? '#D73027':
         value >= 12 ? '#FC8D59':
         value >= 9 ? '#FEE08B':
         value >= 6 ? '#D9EF8B':
         value >= 3 ? '#91CF60':
                      '#1A9850';
}

// Conversion to currency function
function toCurrency(value) {
  value = parseFloat(value);
  
  if (value >= 1000000000) {
    value = value / 1000000000;
    magnitude = 'billion';
  } else {
    value = value / 1000000;
    magnitude = 'million';
  }

  var dollar = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 1,
    maximumFractionDigits: 1
  }).format(value);
  return (dollar + ' ' + magnitude);
}

// Conversion to percentage
function toPercent(value) {
  value = parseFloat(value).toFixed(2);
  return (value + '%');
}

//-----createMap function-------------------
function createMap (expenditures, receipts) {
  
  // Mapbox tile layer function
  function tilelayers (tileid) {
    var tile = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors,\
        <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: tileid,
      accessToken: API_KEY
    });
    return tile;
  }

  // Basemap tile layers
  var streetsbasicmap = tilelayers('mapbox.streets-basic');
  var lightmap = tilelayers('mapbox.light');
  var satellitemap = tilelayers('mapbox.streets-satellite');

  var Stamen_TonerLite = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.{ext}', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    subdomains: 'abcd',
    minZoom: 0,
    maxZoom: 20,
    ext: 'png'
  });

  // Object to hold the base layers
  var baseMaps = {
    "Default": Stamen_TonerLite,
    "Basic": streetsbasicmap,
    "Light": lightmap,
    "Satellite": satellitemap,
  };

  // Create map object with data layers
  var tourismMap = L.map("map", {
    center: [20, 10],
    zoom: 2,
    layers: [
      Stamen_TonerLite,
      expenditures
    ]
  });

  // Object to hold overlay layer
  var overlayMaps = {
    "Tourism Expenditures": expenditures,
    "Tourism Receipts": receipts
  };

  // Layer control
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: true
  }).addTo(tourismMap);

  // Create legend
  var legend = L.control({
    position: 'bottomright'
  });

  // Insert 'legend' div when layer control is added
  legend.onAdd = function(){
    labels = ['Less than 3%', '3% to 6%', '6% to 9%', '9% to 12%', '12% to 15%', '15% or More']
    var div = L.DomUtil.create('div', 'legend');
    div.innerHTML += '<h5>% of Imports/Exports</h5>'
    for (var i = 0; i <= 5; i++) {
      div.innerHTML += '<p><span style="font-size:15px; background-color:' + colorScale(i*3) +
        ';">&nbsp;&nbsp;&nbsp;&nbsp;</span><small> ' + labels[i] + '</small></p>';
    }  
    return div;
  };
  // Add legend
  legend.addTo(tourismMap);
} // end createMap function -------------------

//-----createMarkers function--------------------
function createMarkers(data) {
  
  // Initialize arrays to hold map data
  var expMarkers = [];
  var rctMarkers = [];
  
  // Loop through all countries
  for (var i = 0; i < data.length; i++) {
    country = data[i];

    // Create circle markers for each county and bind a popup with the info
    var expMarker = L.circle([country.latitude, country.longitude], {
      fillOpacity: 0.8,
      color: 'lightslategrey',
      weight: 1,
      fillColor: colorScale(country.expd_pct_imp),
      radius: markerSize(country.expd_total)
    }).bindPopup("<h5>" + country.country_name + "</h5><hr><small>Expenditures: " + 
      toCurrency(country.expd_total) + "<br>of Total Imports: " + 
      toPercent(country.expd_pct_imp) + "</small>");

    var rctMarker = L.circle([country.latitude, country.longitude], {
      fillOpacity: 0.8,
      color: 'lightslategrey',
      weight: 1,
      fillColor: colorScale(country.rcpt_pct_exp),
      radius: markerSize(country.rcpt_total)
    }).bindPopup("<h5>" + country.country_name + "</h5><hr><small>Receipts: " + 
      toCurrency(country.rcpt_total) + "<br>of Total Exports: " + 
      toPercent(country.rcpt_pct_exp) + "</small>");   
    
    // Add markers to arrays
    expMarkers.push(expMarker);
    rctMarkers.push(rctMarker);
  }

  // Create a layer group from the marker arrays and pass to the createMap function
  createMap(L.layerGroup(expMarkers), L.layerGroup(rctMarkers));
} // end createMarkers function -------------------

// GET request for JSON data
d3.json(mapdata_url, createMarkers);