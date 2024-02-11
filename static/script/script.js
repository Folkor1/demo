$(document).ready(function() {

    // Pop-up on hover window
    $(function() {
        var moveLeft = 20;
        var moveDown = 10;
     
        $('a.trigger').hover(function() {
          $('div#pop-up').show();
        }, function() {
          $('div#pop-up').hide();
        });
     
        $('a.trigger').mousemove(function(e) {
          $("div#pop-up").css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
        });
    });

    // Tooltip for edit booking
    $('[data-toggle="tooltip"]').tooltip({
        trigger : 'hover'
    });

    // Loading spinner for admin users table
    $('#user-table, #archive-search-title, #archive-user-table, .swiper-container').delay(200).fadeIn(200); 
    $('#back-button-admin-users, .swiper-container').delay(200).fadeIn(100);
    $('.spinner-div').fadeOut(200);
});