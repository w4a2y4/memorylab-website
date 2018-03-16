let threshold = $('#header').height();

$(window).scroll(function() {
    if ( $(window).scrollTop() > threshold ) {
        if ($('#fixed_head').is(':hidden'))
            $('#fixed_head').fadeIn(200);
    }
    else if ($('#fixed_head').css('opacity') > 0)
        $('#fixed_head').fadeOut(200);
        $('#menu').fadeOut(200);
});

$('#toggle img').click(function(){
    $("#menu").toggle();
});