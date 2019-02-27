// API key
const API_KEY = "pk.eyJ1IjoiZGFydGFuaW9uIiwiYSI6ImNqbThjbHFqczNrcjkzcG10cHpoaWF4aWUifQ.GwBz1hO0sY2QE8bXq9pSRg";

var myMap = L.map("map", {
  center: [37.09, -95.71],
  zoom: 5
});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);


function Color(magnitude) {
   var color = "";
   if (magnitude> 100) {color = "#ea2c2c";}
   else if (magnitude > 75) {color = "#ea822c";}
   else if (magnitude > 50) {color = "#ee9c00";}
   else if (magnitude > 25) {color = "#eecc00";}
   else if (magnitude > 5) {color = "#d4ee00";}
   else {color = "#98ee00";};
   return color;}

function renderData() {
    d3.json(`/states`, function(data) {
      console.log(data)

      for (var i = 0; i < data.length; i++) {
        L.circle([data[i].latitude, data[i].longitude], {
            fillOpacity: 0.75,
            color: "white",
            fillColor: Color(data[i].count),
            radius: data[i].count * 1000
          }).bindPopup("<h1>" + data[i].state + "</h1> <hr> <h3>Players: " + data[i].count + "</h3>").addTo(myMap);
      }
    })
}

$(function() {
    renderData();
});