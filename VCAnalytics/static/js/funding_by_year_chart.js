
//Plotly.d3.csv('../VCdatabaseLat.csv', function (data){
//Importar informacion
//function buildMetadata(sample) {
//}
function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function buildCharts() {

    var url = "https://venture-capital.herokuapp.com/FundingByYearCountry";
    d3.json(url).then(function (data) {

        data_trace = []
        for (var iter = 0; iter < data.length; iter++) {

            var trace = {
                x: Object.keys(data[iter]["data_by_year"]).slice(1),
                y: Object.values(data[iter]["data_by_year"]).slice(1),
                name: data[iter]['country'],
                marker: {
                    color: getRandomColor(),
                    size: Object.values(data[iter]["data_by_year"]).slice(1),
                    sizemode: 'area',
                },
                mode: 'markers',
            };
            data_trace.push(trace);

        }
        var layout = {
        hovermode: 'closest',
        plot_bgcolor: 'rgb(250, 250, 250)',

        xaxis: {
            gridcolor: '#FFFFFF',
            title: 'Funded Date'
        },
        yaxis: {
            gridcolor: '#FFFFFF',
            title: 'Total Funding',
            type: 'box'
        }
    }
    Plotly.newPlot('plotly-div', data_trace, layout);

    });
}
  