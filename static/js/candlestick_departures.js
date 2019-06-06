var TDDURL = "/tourism_departure_data";
d3.json(TDDURL, function(data) {
  var data = [data];
  var layout = {
    yaxis: { title: "No. of Departures (2008 - 2017)",
    autorange: true,
    type: "linear" }
  };
  Plotly.plot("plot", data, layout);
});
