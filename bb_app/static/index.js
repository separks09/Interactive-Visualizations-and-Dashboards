Plotly.d3.json("http://127.0.0.1:5000/names", function(error,data) {
    if (error) console.error;
    console.log(data);

    var select = document.getElementById('selDataset');

    for (var i = 0; i < data.length; i++) {
        var option = document.createElement('option');
        option.innerHTML = data[i];
        option.value = data[i];
        select.appendChild(option);
};

});     

var a = document.getElementById('selDataset');
var sample = a.options[a.selectedIndex].value;

Plotly.d3.json("http://127.0.0.1:5000/metadata/"+sample+'"', function(error,data) {
    if (error) console.error;
    console.log(data);

    var metadata = documant.getElementById("metadata");
    metadata.innerHTML = data[i];

});   


