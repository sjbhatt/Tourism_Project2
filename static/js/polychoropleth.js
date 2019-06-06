var polygonData = [];
var minValue = 0;
var maxValue = 0;

var queryUrl = "http://127.0.0.1:5000/arriv_dep_data";
function getDataFromLocal(arrivalsDep){
    d3.json(queryUrl, function(data) {
        // Once we get a response, send the data.features object to the createFeatures function
        populateData(data, arrivalsDep);
    });
}

function populateData(data, arrivalsDep){
    for(i=0;i< data.length ; i++){
      var currValue = arrivalsDep ? data[i].arrivals : data[i].departures;
      if(minValue > currValue)
        minValue = currValue;
      if(maxValue < currValue)
        maxValue = currValue
      var data1 = {
        id : countryISOMapping[data[i].country_iso],
        value : currValue
      }
      polygonData.push(data1);
    }
    mapsInitialize();
}

function mapsInitialize(){
  am4core.ready(function() {

  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end

  // Create map instance
  var chart = am4core.create("chartdiv", am4maps.MapChart);

  // Set map definition
  chart.geodata = am4geodata_worldLow;

  // Create map polygon series
  var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

  //Set min/max fill color for each area
  polygonSeries.heatRules.push({
    property: "fill",
    target: polygonSeries.mapPolygons.template,
    min: chart.colors.getIndex(10).brighten(1),
    max: chart.colors.getIndex(10).brighten(-0.3)
    // min: am4core.color("#ffffff"),
    // max: am4core.color("#AAAA00")
  });

  // Make map load polygon data (state shapes and names) from GeoJSON
  polygonSeries.useGeodata = true;

  polygonSeries.data = polygonData;

  // Set up heat legend
  let heatLegend = chart.createChild(am4maps.HeatLegend);
  heatLegend.series = polygonSeries;
  heatLegend.align = "left";
  heatLegend.valign = "middle";
  heatLegend.width = am4core.percent(100);
  //heatLegend.marginRight = am4core.percent(4);
  heatLegend.minValue = 0;
  heatLegend.maxValue = 87000000;
  heatLegend.orientation = "vertical";
  //heatLegend.padding(20, 20, 20, 20);
  heatLegend.valueAxis.renderer.labels.template.fontSize = 15;
  heatLegend.valueAxis.renderer.minGridDistance = 10;


  polygonSeries.mapPolygons.template.events.on("over", event => {
    handleHover(event.target);
  });

  polygonSeries.mapPolygons.template.events.on("hit", event => {
    handleHover(event.target);
  });

  function handleHover(mapPolygon) {
    if (!isNaN(mapPolygon.dataItem.value)) {
      heatLegend.valueAxis.showTooltipAt(mapPolygon.dataItem.value);
    } else {
      heatLegend.valueAxis.hideTooltip();
    }
  }

  polygonSeries.mapPolygons.template.strokeOpacity = 0.4;
  polygonSeries.mapPolygons.template.events.on("out", event => {
    heatLegend.valueAxis.hideTooltip();
  });

  // Set up custom heat map legend labels using axis ranges
  var minRange = heatLegend.valueAxis.axisRanges.create();
  minRange.value = heatLegend.minValue;
  minRange.label.text = minValue; //"Less Visitors";
  var maxRange = heatLegend.valueAxis.axisRanges.create();
  maxRange.value = heatLegend.maxValue;
  maxRange.label.text = maxValue; //"More Vistors!";

  // Blank out internal heat legend value axis labels
  heatLegend.valueAxis.renderer.labels.template.adapter.add("text", function(labelText) {
    return "";
  });

  // Configure series tooltip
  var polygonTemplate = polygonSeries.mapPolygons.template;
  polygonTemplate.tooltipText = "{name}: {value}";
  polygonTemplate.nonScalingStroke = true;
  polygonTemplate.strokeWidth = 0.5;
  
  // Create hover state and set alternative fill color
  var hs = polygonTemplate.states.create("hover");
  hs.properties.fill = am4core.color("#3c5bdc"); //#3c5bdc

  chart.zoomControl = new am4maps.ZoomControl();
  chart.zoomControl.valign = "top";

  polygonSeries.exclude = ["AQ"];


  }); // end am4core.ready()
}
