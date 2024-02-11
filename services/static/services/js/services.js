$(document).ready(function() {

    // Expiry timer
    if ($('#expiry_timer').attr('data')) {
        var timer2 = $('#expiry_timer').attr('data');
        var interval = setInterval(function() {
        var timer = timer2.split(':');
        var minutes = parseInt(timer[0], 10);
        var seconds = parseInt(timer[1], 10);
        --seconds;
        minutes = (seconds < 0) ? --minutes : minutes;
        seconds = (seconds < 0) ? 59 : seconds;
        reverse_counter = minutes * 60 + seconds // progress bar
        document.getElementById("pbar").value = 300 - --reverse_counter; // progress bar
        seconds = (seconds < 10) ? '0' + seconds : seconds;
        $('.countdown').html(minutes + ':' + seconds);
        if (minutes < 0) clearInterval(interval);
        if ((seconds <= 0) && (minutes <= 0)) return timer2 = '5:00';
        timer2 = minutes + ':' + seconds;
        }, 1000);
    };

    // Duplicates timer
    if ($('#expiry_timer_dupes').attr('data')) {
        var timer3 = $('#expiry_timer_dupes').attr('data');
        var interval = setInterval(function() {
        var timer = timer3.split(':');
        var minutes = parseInt(timer[0], 10);
        var seconds = parseInt(timer[1], 10);
        --seconds;
        minutes = (seconds < 0) ? --minutes : minutes;
        seconds = (seconds < 0) ? 59 : seconds;
        reverse_counter = minutes * 60 + seconds // progress bar
        document.getElementById("pbar_dupes").value = 600 - --reverse_counter; // progress bar
        seconds = (seconds < 10) ? '0' + seconds : seconds;
        $('.countdown-dupes').html(minutes + ':' + seconds);
        if (minutes < 0) clearInterval(interval);
        if ((seconds <= 0) && (minutes <= 0)) return timer3 = '10:00';
        timer3 = minutes + ':' + seconds;
        }, 1000);
    };
});