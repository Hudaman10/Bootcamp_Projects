$(function() {
  console.log('jquery is working!');
  createGraph();
});

function createGraph() {

var svgWidth = 3000;
var svgHeight = 660;

var color = d3.scale.category20();

// Define the chart's margins as an object
var chartMargin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

// Define dimensions of the chart area
var chartWidth = svgWidth - chartMargin.left - chartMargin.right;
var chartHeight = svgHeight - chartMargin.top - chartMargin.bottom;

// Select body, append SVG area to it, and set the dimensions
var svg = d3.select("#chart")
  .append("svg")
  .attr("height", svgHeight)
  .attr("width", svgWidth);

// Append a group to the SVG area and shift ('translate') it to the right and to the bottom
var chartGroup = svg.append("g")
  .attr("transform", `translate(${chartMargin.left}, ${chartMargin.top})`);


// Load data from data.csv
d3.json(`/colleges`, function(Data) {

  console.log(Data);


   // Cast the poverty and healthcare values to a number for each piece of Data
  Data.forEach(function(data) {
    data.player_count = +data.player_count;
  });

// Configure a band scale for the horizontal axis with a padding of 0.1 (10%)
  var xBandScale = d3.scaleBand()
    .domain(Data.map(d => d.college))
    .range([0, chartWidth])
    .padding(0.1);
    

  // Create a linear scale for the vertical axis.
  var yLinearScale = d3.scaleLinear()
    .domain([0, d3.max(Data, d => d.player_count)])
    .range([chartHeight, 0]);

  // Create two new functions passing our scales in as arguments
  // These will be used to create the chart's axes
  var bottomAxis = d3.axisBottom(xBandScale);
  var leftAxis = d3.axisLeft(yLinearScale).ticks(15);

  // Append two SVG group elements to the chartGroup area,
  // and create the bottom and left axes inside of them
  chartGroup.append("g")
    .call(leftAxis);

  chartGroup.append("g")
    .attr("transform", `translate(0, ${chartHeight})`)
    .call(bottomAxis);

  
  // Use the linear and band scales to position each rectangle within the chart
  var barGroup = chartGroup.selectAll(".bar")
    .data(Data)
    .enter()
    .append("rect")
    .attr("class", "bar")
    .attr("x", d => xBandScale(d.college))
    .attr("y", d => yLinearScale(d.player_count))
    .attr("width", xBandScale.bandwidth())
    .attr("height", d => chartHeight - yLinearScale(d.player_count));
    

  chartGroup.append("text")
    // Position the text
    // Center the text:
    .attr("transform", `translate(${chartWidth / 2}, ${chartHeight + chartMargin.top + 20})`)
    .attr("text-anchor", "middle")
    .attr("font-size", "16px")
    .text("College");

   // append y axis
  chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - chartMargin.left)
    .attr("x", 0 - (chartHeight / 2))
    .attr("dy", "1em")
    .classed("axis-text", true)
    .text("Player Count");

  var toolTip = d3.select("body")
    .append("div")
    .classed("tooltip", true);

  barGroup.on("mouseover", function(d) {
    toolTip.style("display", "block")
        .html(
          `<strong>${(d.college)}<strong><hr>${d.player_count}
      Players`)
        .style("left", d3.event.pageX + "px")
        .style("top", d3.event.pageY + "px");
  })
    // Step 3: Create "mouseout" event listener to hide tooltip
    .on("mouseout", function() {
      toolTip.style("display", "none");
    });

});

}