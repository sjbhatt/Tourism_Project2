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
