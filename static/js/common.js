let threshold = $('#header').height();

$('#fixed_head').hide();

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


$('#file-upload').change(function() {
    var filepath = this.value;
    var m = filepath.match(/([^\/\\]+)$/);
    var filename = m[1];
    $('#filename').html(filename);

});