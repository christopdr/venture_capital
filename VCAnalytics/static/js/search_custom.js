//search sample data
//search_data= ["bootstrap", "bootstrap grid","bootstrap nav","bootstrap template","bootstrap examples","bootstrap for dummy","bootstrap labels", "bootstrap buttons"];


$(document).ready(function(){
   $("#searchMatch").on("keyup", function (event) {
       // do whatever you need
       $('#sugestion-container-data').html('');
       $("#suggestion-display").css("visibility", "visible");
       if ($("#searchMatch").val()) {
           $.ajax({
               url: "https://venture-capital.herokuapp.com/searchCompany/" + $("#searchMatch").val(),
               success: function (search_data) {
                   for (var i = 0; i < search_data.length; i++) {
                       $('#sugestion-container-data').append("<li onclick='getCompanySelected(this)' class='list-group-item custom-li'>" + search_data[i] + "</li>");
                   }
               }
           });
       }


   });
    $("body").click(function(){
        $("#suggestion-display").css("visibility", "hidden");
       // $('#sugestion-container-data').html('');
    });

    $('#search_btn').click(function () {
        var word = $('#searchMatch');
        if (word) {
            $.ajax({
                url: "https://venture-capital.herokuapp.com/searchCompanyData/" + $("#searchMatch").val(),
                success: function (search_data) {
                    console.log(search_data);
                    $('#company_name').text(search_data[0]['Company Name']);
                    $('#company_description').text(search_data[0]['Company Business Description']);
                    if(search_data[0]['Company Founded Date']){
                        var split_d = search_data[0]['Company Founded Date'].split('/');
                        if(split_d.length == 3){
                            $('#company_foundation').text(split_d[2]);
                        }
                        else{
                            $('#company_foundation').text('Not Available');
                        }
                       }

                    $('#foundation_money').text('$ ' + search_data[0]['Total Funding To Date (USD) Mil'] + ' M');
                    $('#foundation_country').text(search_data[0]['Company Nation']);
                    $('#foundation_industry').text(search_data[0]['Industry']);
                    $('#company-data').css('visibility','visible');
                }
            });
        }
    });

});

function getCompanySelected(element){
    $('#searchMatch').val(element.innerHTML);
}
