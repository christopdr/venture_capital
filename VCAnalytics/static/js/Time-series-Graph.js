
//Plotly.d3.csv('../VCdatabaseLat.csv', function (data){
//Importar informacion
//function buildMetadata(sample) {
//}

function buildCharts() {

    var url = "https://venture-capital.herokuapp.com/FundingByYear";
    d3.json(url).then(function (data) {
        
        //var industry = [];
        var y_values = [];
        var x_values = [];
        
        for(var i = 0; i < data.length - 1; i++){
            //industry.push(data[i]["VE Industry Description"]);
            y_values.push(parseFloat(data[i]["total"]));
            x_values.push(String(data[i]["year"]));
        }
        

    console.log(x_values);

    var trace1 = {
        x: x_values,
        y: y_values,
        marker: {
            color: 'rgb(171, 99, 250)',
            size: y_values,
            sizemode: 'area',
        },
        mode: 'markers',
    }

    var data = [trace1];

    var layout = {
        title: 'LATAM Total Funding per Year (USD)',
        hovermode: 'closest',
        plot_bgcolor: 'rgb(223, 232, 243)',

        xaxis: {
            gridcolor: '#FFFFFF',
            title: 'Funded Date (Year)'
        },
        yaxis: {
            gridcolor: '#FFFFFF',
            title: 'Total Funding (MM USD)',
            type: 'box'
        }
    }
    Plotly.newPlot('plotly-div', data, layout);
});
}
//Plotly.newPlot('plotly-div', {
  //data: data,
  //layout: layout
  //frames: frames
//});

//var frame1 = {
    //data: [
      //{
        //x: [28.801, 50.93899999999999, 37.484, 39.417, 44.0, 60.96, 37.373000000000005, 37.468, 44.869, 45.32, 65.39, 63.03, 43.158, 50.056000000000004, 47.453, 55.565, 55.928000000000004, 48.463, 42.244, 36.319, 36.157, 37.578, 43.43600000000001, 47.751999999999995, 39.875, 60.396, 57.593, 45.883, 58.5, 50.848, 40.412, 43.16, 32.548], 
        //y: [779.4453145, 9867.084765000001, 684.2441716, 368.46928560000003, 400.44861069999996, 3054.421209, 546.5657493, 749.6816546, 3035.326002, 4129.766056, 4086.522128, 3216.956347, 1546.907807, 1088.277758, 1030.592226, 108382.3529, 4834.804067, 1831.132894, 786.5668575, 331.0, 545.8657228999999, 1828.230307, 684.5971437999999, 1272.880995, 6459.5548229999995, 2315.138227, 1083.53203, 1643.485354, 1206.947913, 757.7974177, 605.0664917, 1515.5923289999998, 781.7175761], 
        //marker: {
          //color: 'rgb(171, 99, 250)', 
          //size: [8425333.0, 120447.0, 46886859.0, 4693836.0, 556263528.0, 2125900.0, 372000000.0, 82052000.0, 17272000.0, 5441766.0, 1620914.0, 86459025.0, 607914.0, 8865488.0, 20947571.0, 160000.0, 1439529.0, 6748378.0, 800663.0, 20092996.0, 9182536.0, 507833.0, 41346560.0, 22438691.0, 4005677.0, 1127000.0, 7982342.0, 3661549.0, 8550362.0, 21289402.0, 26246839.0, 1030585.0, 4963829.0], 
          //sizemode: 'area', 
          //sizeref: 200000, 
          //sizesrc: 'PythonPlotBot:2476:bf9a58'
        //}, 
        //mode: 'markers', 
        //name: 'Asia', 
        //text: ['Afghanistan', 'Bahrain', 'Bangladesh', 'Cambodia', 'China', 'Hong Kong, China', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan', 'Korea, Dem. Rep.', 'Korea, Rep.', 'Kuwait', 'Lebanon', 'Malaysia', 'Mongolia', 'Myanmar', 'Nepal', 'Oman', 'Pakistan', 'Philippines', 'Saudi Arabia', 'Singapore', 'Sri Lanka', 'Syria', 'Taiwan', 'Thailand', 'Vietnam', 'West Bank and Gaza', 'Yemen, Rep.'], 
        //textsrc: 'PythonPlotBot:2476:dce10d', 
        //type: 'scatter', 
        //xsrc: 'PythonPlotBot:2476:a43382', 
        //ysrc: 'PythonPlotBot:2476:9e7f0b'
      //}, 
    //], 
    //name: '1952'
  //};

//frames = [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, frame9, frame10, frame11];