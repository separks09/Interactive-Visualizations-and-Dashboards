var graphDiv = document.getElementById("pie")

var data = [{
  values: [1,4,7,9],
  labels: ["test1", "test2", 'test3', "test4"],
  type: "pie"
}];

  var layout = {
    title:  "Type and percent of bateria in sample",
  };

Plotly.plot(graphDiv, data, layout);


function optionChanged(value){
  var select = document.getElementById('selDataset');
}

Plotly.d3.json('/line', function(error, data){
  if (error) return console.warn(error);

  var layout = { margin: { t: 0 } }
  var LINE = document.getElementById('line');
  Plotly.plot(LINE, data)
})