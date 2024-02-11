$(document).ready(function() {

    let pianoOrTheory = document.getElementById("piano-or-theory");
    let onlineorOffline = document.getElementById("online-or-offline");
    let lesson = document.getElementById("lesson-confirmation");
    let lessonType = document.getElementById("lesson-type-confirmation");
    let selectDate = document.getElementById("date-confirmation");
    let selectTime = document.getElementById("time-confirmation");
    let editDateDate = document.getElementById("edit-date-date");
    let editDateTime = document.getElementById("edit-time");
    let editLessonType = document.getElementById("edit_lesson_type");
    let bookingForDate = document.getElementById("booking-for-date");
    let booking = [];
    let date = [];
    let time = [];

    // Change lesson type options when clicked
    $("#piano-btn").on("click", function() {
        $("#piano-theory").addClass("d-none");
        $("#book-for").removeClass("d-none");
        $("#select-lesson-type").removeClass("d-none");
        $("#oo-buttons").removeClass("d-none");
        booking.push('Piano');
        pianoOrTheory.innerText = booking[0];
    });

    $("#theory-btn").on("click", function() {
        $("#piano-theory").addClass("d-none");
        $("#book-for").removeClass("d-none");
        $("#select-lesson-type").removeClass("d-none");
        $("#oo-buttons").removeClass("d-none");
        $("#theory").removeClass("d-none");
        booking.push('Theory');
        pianoOrTheory.innerText = booking[0];
    });

    // Change online/offline options when clicked
    $("#online-btn").on("click", function() {
        $("#select-lesson-type").addClass("d-none");
        $("#oo-buttons").addClass("d-none");
        $("#select-date").removeClass("d-none");
        $("#calendar").removeClass("d-none");
        $('#online').removeClass("d-none");
        booking.push('Online');
        onlineorOffline.innerText = booking[1];
    });

    $("#offline-btn").on("click", function() {
        $("#select-lesson-type").addClass("d-none");
        $("#oo-buttons").addClass("d-none");
        $("#select-date").removeClass("d-none");
        $("#calendar").removeClass("d-none");
        $('#offline').removeClass("d-none");
        booking.push('Offline');
        onlineorOffline.innerText = booking[1];
    });

    // Back to lesson selection
    $("#back-lesson").on("click", function() {
        $("#select-lesson-type").addClass("d-none");
        $("#piano-theory").removeClass("d-none");
        $("#book-for").addClass("d-none");
        $("#oo-buttons").addClass("d-none");
        $("#piano").addClass("d-none");
        $("#theory").addClass("d-none");
        booking.splice(booking.indexOf('Piano', 'Theory'),1);
        onlineorOffline.innerText = "";
    });

    // Back to lesson type selection
    $("#back-lesson-type").on("click", function() {
        $("#calendar").addClass("d-none");
        $("#select-lesson-type").removeClass("d-none");
        $("#select-date").addClass("d-none");
        $("#oo-buttons").removeClass("d-none");
        $('#online').addClass("d-none");
        $('#offline').addClass("d-none");
        $('#select-time').addClass('d-none');
        booking.splice(booking.indexOf('Online', 'Offline'),1);
        onlineorOffline.innerText = "";
    });

    // Back to date selection
    $("#back-select-date").on("click", function() {
        $("#calendar").removeClass("d-none");
        $("#back-select-date").addClass("d-none");
        $("#select-time").addClass("d-none");
        $("#select-date").removeClass("d-none");
        $('td').removeClass("active");
        $("#booking-for-date").addClass('d-none');
        $("#at-icon").addClass('d-none');
        $('#time-picker').addClass('d-none');
        $('#book-div').addClass('d-none');
        $('input[type="radio"]').prop('checked', false);
        $('.time-btns').removeClass('disabled');
        $('.all-times-booked').addClass('d-none');
    });

    // Display time picker once date is selected
    $('#date').datepicker().on('changeDate', function() {
        $('#time-picker').removeClass('d-none');
        $('#select-time').removeClass('d-none');
        $("#select-date").addClass("d-none");
        $("#calendar").addClass('d-none');
        $("#back-select-date").removeClass('d-none');
        $("#booking-for-date").removeClass('d-none');
        $("#at-icon").removeClass('d-none');
    });

    // Display Book button once time is selected
    $('#time-picker').change(function() {
        $('#book-div').removeClass('d-none');
        time.splice(0);
        var selectedTime = $('input[type="radio"]:checked+label').text()
        time.push(selectedTime);
    });

    // Get date from the calendar
    $('#date').datepicker().on('changeDate', function (selectedDate) {
        date.splice(0);
        var readableDate = selectedDate.date.toDateString();
        bookingForDate.innerText = readableDate;

        // Display 17:00 button when Monday is selected
        if ($('#booking-for-date').is(':contains("Mon")')) {
            $(".time-17").removeClass('d-none');
        } else {
            $(".time-17").addClass('d-none');
        };

        // Hide 16:00 button when Friday is selected
        if ($('#booking-for-date').is(':contains("Fri")')) {
            $(".time-16").addClass('d-none');
        } else {
            $(".time-16").removeClass('d-none');
        };
        selectedDate = selectedDate.date.toLocaleDateString('en-CA');
        date.push(selectedDate);

        // Disable booked time buttons
        var clip = new Date(readableDate).toDateString();
        var form = clip.toString().slice(4, 20).replace(/ /, '. ').replace(/ 0/, ' ');
        var lIndex  = form.lastIndexOf(" ");
        form = form.substring(0, lIndex) + ", " + form.substring(lIndex + 1);
        var datetime_ten = form;
        var date_all_times = [];
        var actual_times = [];
        var ids = [];
        const divs = document.getElementsByClassName('time-btns');
        const times = document.getElementsByClassName('hide-time');
        for (let x = 0; x < divs.length; x++) {
            var spliced_time = divs[x].innerText.slice(0, 2)
            if (spliced_time == '10') {
                spliced_time = '10 a.m.'
            } else if (spliced_time == '11') {
                spliced_time = '11 a.m.'
            } else if (spliced_time == '12') {
                spliced_time = 'noon'
            } else if (spliced_time == '14') {
                spliced_time = '2 p.m.'
            } else if (spliced_time == '15') {
                spliced_time = '3 p.m.'
            } else if (spliced_time == '16') {
                spliced_time = '4 p.m.'
            } else if (spliced_time == '17') {
                spliced_time = '5 p.m.'
            };
            date_all_times.push(datetime_ten + " " + spliced_time);
            };
        for (let x = 0; x < times.length; x++) {
            actual_times.push(times[x].innerText)
        };
        const intersection = actual_times.filter(element => date_all_times.includes(element));
        for (let x = 0; x < intersection.length; x++) {
            ids.push(intersection[x].slice(13, 21).replace(/^\s+|\s+$/g, ""))
        };
        for (let x = 0; x < ids.length; x++) {
            var bts = document.getElementById(ids[x])
            $(bts).addClass('disabled')
        };

        // Show notification if all times booked for the day
        if (document.getElementsByClassName('disabled time-btns').length == $('.time-btns:visible').length) {
            $('.all-times-booked').removeClass('d-none')
        };
    });

    // Get selections lesson types from booking menus
    function getLesson() {
        lesson.innerText = booking[0];
        document.getElementById('lesson_inp').value = booking[0];
    };

    function getLessonType() {
        lessonType.innerText = booking[1];
        document.getElementById('lesson_type_inp').value = booking[1];
    };

    function getDate() {
        selectDate.innerText = date[0];
        document.getElementById('date_inp').value = date[0];
    };

    // Get time from time picker
    function getTime() {
        selectTime.innerText = time[0];
        document.getElementById('time_inp').value = time[0];
    };

    // Booking confirmation message
    $('#book-confirm').on("click", function() {
        $('#confirm-message').removeClass('d-none');
        $('#calendar').addClass('d-none');
        $('#select-date').addClass('d-none');
        $('#book-for').addClass('d-none');
        getLesson();
        getLessonType();
        getDate();
        getTime();
    });

    // Timeout for alert messages
    setTimeout(function() {
        $(".alert").alert('close');
    }, 2000);

    // Edit date confirmation message
    $('#edit-book-confirm').on("click", function() {
        $('#edit-date-time').addClass('d-none');
        $('#edit-date-form').removeClass('d-none');
        getDateDate();
        getDateTime();
    });

    // Edit date - back button
    $('#edit-date-back-to-selection').on("click", function() {
        $('#edit-date-form').addClass('d-none');
        $('#edit-date-time').removeClass('d-none');
    });

    // Change type - hide buttons
    $('#change-type, #cancel').on("click", function() {
        window.addEventListener('DOMContentLoaded', function() {
            $('#manage-bookings-sub-wrap').addClass('d-none');
        });
    });

    // Get date from date picker on edit
    function getDateDate() {
        editDateDate.innerText = date[0];
        document.getElementById('edit_date_inp').value = date[0];
    };

    // Get time from time picker on edit
    function getDateTime() {
        editDateTime.innerText = time[0];
        document.getElementById('edit_time_inp').value = time[0];
    };

    // Get lesson type on edit
    $('#edit-lesson-type-confirm').on("click", function() {
        if($("#edit_type_value").is(':contains("Online")')) {
            editLessonType.value = 'Online';
        } else {
            editLessonType.value = 'Offline';
        };
    });

    // Show modal when edit lesson type page opens
    if (window.location.href.indexOf("edit_type")) {
        $('#edit-lesson-type').modal('show');
    };

    // Show modal when cancel page opens
    if (window.location.href.indexOf("cancel")) {
        $('#cancel-lesson').modal('show');
    };

    // Reload page when hiding modal
    $('#edit-date-form, #confirm-message').on('hidden.bs.modal', function () {
        location.reload();
    });

    $('#edit-lesson-type, #cancel-lesson').on('hidden.bs.modal', function () {
        history.go(0);
    });

    // Show / hide booking edit buttons
    $('.edit-toggle-button').on("click", function() {
        var clicked = $(this).attr('label');
        var expand = document.getElementById(clicked);
        if ($(expand).hasClass('d-none')) {
            $("[id*='ed']").addClass("d-none");
            $(expand).removeClass("d-none");
        } else {
            $(expand).addClass("d-none");
        };
    });
});