var TADURL = "/tourism_arrival_data";
d3.json(TADURL).then(function(data) {
  var data = [data];
  var layout = {
    title: `Tourism Arrivals`,
    yaxis: { title: "No. of Arrivals (2008 - 2017)",
    autorange: true,
    type: "linear" }
  };
  Plotly.plot("plot", data, layout);
});

/*

var TDDURL = "/tourism_departure_data";
d3.json(TDDURL).then(function(data) {
  var data = [data];
  var layout = {
    title: `Tourism Departures`,
    yaxis: { title: "No. of Departures (2008 - 2017)",
    autorange: true,
    type: "linear" }
  };
  Plotly.plot("plot", data, layout);
});

*/