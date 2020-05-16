ajaxURL = 'http://' + location.host

//alert (ajaxURL)

function getGrab(img) {
        $("#big").empty();
        $big = ( '<img height="360" width="640" src="' + ajaxURL + '/get_grab/' + img + '"></img>' );
            
        $("#big").append($big);

        $("#big").click(function () {
                $("#big").empty();
         });

}

function getGrabs() {
     $.getJSON(ajaxURL + '/get_grabs', function(data) {
        $("#grabs").empty();
        $.each(data, function (i,v) {
          
            $grab = $('<img height="72" width="128" src="' + ajaxURL + '/get_grab/' + v + '"></img>').append(v);
            $grab.click(function () {
                getGrab(v);
            });
           $("#grabs").append($grab);
        });
    });
}

$(document).ready(function() {


    getGrabs();


});
