

const url = "https://venture-capital.herokuapp.com/topFundingByCountry";
d3.json(url).then(function(data) {

// Sort the data array
//latam.sort(function(a, b) {
//    return parseFloat(b.Funding) - parseFloat(a.Funding);
//  });


// Slice for plotting
//data = latam.slice(0, 5);

// Trace1 for the Data
    funding =[];
    country= [];
    for(var x  = 0; x < 5; x++){
        funding.push(parseFloat(data[x]["Funding"]));
        country.push(data[x]["Country"]);
    }

    var trace1 = {
        x: country,
        y: funding,
        text: country,
        name: "Country",
        type: "bar",
        orientation:"v",
        width:[0.4,0.4,0.4,0.4,0.4],
        marker: {
          color: ['rgb(232, 62, 140)','rgb(111, 66, 193)','rgb(111, 66, 193)','rgb(111, 66, 193)','rgb(111, 66, 193)']
        }
      };


    // set up the data variable
    var data = [trace1];


    // set up the layout variable

    var layout = {
        title: "Top Countries with more funding ",
        'yaxis': {'title': '(USD) Mil'},
      };

    // Render the plot to the div tag with id "plot"
    Plotly.newPlot("plot_country", data, layout);

  });

/*$.ajax({url: "https://venture-capital.herokuapp.com/getData",
          success: function(data){
                //$("#div1").html(result);
              console.log(data);
          }
});
*/
