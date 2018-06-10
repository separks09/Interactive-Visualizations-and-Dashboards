

var jsonUrl = "http://127.0.0.1:5000/samples/BB_952"

Plotly.d3.json(jsonUrl, function(error,data) {
    if (error) console.error;
    console.log(data);
    
    dataTopTen = [];
    for (var i = 0; data.length < 10; i++){
      dataTopTen.append(data[i])
    };

});


function init() {
    var data = [{
      values: [1,4,7,9],
      labels: ["test1", "test2", 'test3', "test4"],
      type: "pie"
    }];
  
    var layout = {
      title:  "Type and percent of bateria in sample",
    };
  
    Plotly.plot("#pie", data, layout);
  }
  





  function updatePlotly(newdata) {
    var PIE = document.getElementById("pie");
    Plotly.restyle(PIE, "values", [newdata]);
  }
  
  function getData(dataset) {
    var data = [];
    switch (dataset) {
    case "dataset1":
      data = [1, 2, 3, 39];
      layout = {
        title:  "% of App Usage per Country",
        height: 600,
        width: 800};
      break;
    case "dataset2":
      data = [10, 20, 30, 37];
      layout = {
        title:  "% of App Usage per Country",
        height: 600,
        width: 800};
      break;
    case "dataset3":
      data = [100, 200, 300, 23];
        layout = {
        title:  "% of App Usage per Country",
        height: 600,
        width: 800};
      break;
    default:
      data = [0, 0, 0, 0];
      layout = {
        title:  "% of App Usage per Country",
        height: 600,
        width: 800};
    }
  
    
    updatePlotly(data);
  }
  
  init();
  