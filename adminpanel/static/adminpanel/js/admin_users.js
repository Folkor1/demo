$(document).ready(function() {

    let userId = document.getElementById("user-id");
    let userIdInact = document.getElementById("user-id-inact");
    let userIdDel = document.getElementById("user-id-del");
    let reviewStatus = document.getElementById("admin-status-submit")
    let reviewId = document.getElementById("admin-status-id")
    let finStatus = document.getElementById("admin-fin-submit")
    let finId = document.getElementById("admin-fin-id")
    let bulk_confirm = document.getElementById("bulk-confirm-user-id")
    let bulk_to_pending = document.getElementById("bulk-to-pending-user-id")
    let bulk_cancel = document.getElementById("bulk-cancel-user-id")
    let bulk_finalize = document.getElementById("bulk-finalize-user-id")
    let bulk_discard = document.getElementById("bulk-discard-user-id")
    let ids = [];
    let review_ids = []
    let usernames_pending = [];
    let usernames_approved = [];
    let usernames_all = [];

    // Hide modal and redirect
    $("#activate-users, #inactivate-users, #delete-users").on('hidden.bs.modal', function () {
        document.location.href = '/admin_users';
    });

    // Tick all check boxes on table
    $("#check-all-boxes, #review-check-all-boxes").click(function () {
        $(".form-check-input").prop('checked', $(this).prop('checked'));
        if ($(this).is(':checked')) {
            var checkedValue = $('.check:checked');
            for (let i = 0; i < checkedValue.length; i++) {
                var all_ids = $(checkedValue[i]).closest("th").find("[name='get-id-by-js']").attr('label');
                var all_usernames = $(checkedValue[i]).closest("th").find("[name='get-value-by-js']").attr('label');
                var all_statuses = $(checkedValue[i]).closest("th").find("[name='get-status-by-js']").attr('label');
                var review_bulk_ids = $(checkedValue[i]).closest("th").find("[name='review-get-id-by-js']").attr('label');
                if (all_statuses) {
                    if (all_statuses.includes('Pending') && !usernames_pending.includes(all_usernames)) {
                        usernames_pending.push(all_usernames)
                    };
                    if (all_statuses.includes('Approved') && !usernames_approved.includes(all_usernames)) {
                        usernames_approved.push(all_usernames)
                    };
                    if (!usernames_all.includes(all_usernames)) {
                        usernames_all.push(all_usernames)
                    };
                };
            ids.push(all_ids);
            review_ids.push(review_bulk_ids);
            };
        } else {
            ids = [];
            usernames_pending = [];
            usernames_approved = [];
            usernames_all = [];
            review_ids = [];
        };
    });

    // Get checked boxes ids
    $("[id$='selected']").click(function() {
        var checked = $(this).is(':checked')
        var parent = $(this).closest("th").find("[name='get-id-by-js']").attr('label');
        var review_id = $(this).closest("th").find("[name='review-get-id-by-js']").attr('label');

        // Admin users table
        if (checked) {
            ids.push(parent);
            review_ids.push(review_id);
        } else {
            ids.splice(ids.indexOf(parent),1);
            review_ids.splice(review_ids.indexOf(review_id),1);
        };
    });

    // Get checked boxes usernames
    $('input:checkbox').change(function() {
        var checked_users = $(this).is(':checked')
        var find_username = $(this).closest("th").find("[name='get-value-by-js']").attr('label');
        var check_status = $(this).closest("th").find("[name='get-status-by-js']").attr('label');
        if (check_status) {

            // Get usernames with Pending status
            if (check_status.includes('Pending') && checked_users && !usernames_pending.includes(find_username)) {
                usernames_pending.push(find_username)
            } else if (check_status.includes('Pending') && usernames_pending.includes(find_username)) {
                usernames_pending.splice(usernames_pending.indexOf(find_username),1);
            };

            // Get usernames with Approved status
            if (check_status.includes('Approved') && checked_users && !usernames_approved.includes(find_username)) {
                usernames_approved.push(find_username)
            } else if (check_status.includes('Approved') && usernames_approved.includes(find_username)) {
                usernames_approved.splice(usernames_approved.indexOf(find_username),1);
            };

            // Get usernames with all statuses
            if (checked_users && !usernames_all.includes(find_username)) {
                usernames_all.push(find_username)
            } else {
                usernames_all.splice(usernames_all.indexOf(find_username),1);
            };
        };
    });

    // Store user ids when redirecting to activate user page
    $("#activate-modal, #inactivate-modal, #delete-modal").click(function () {
        localStorage.setItem("storagedIds", ids);
        localStorage.setItem("storagedUserNames", usernames_pending);
        localStorage.setItem("storagedUserNamesApproved", usernames_approved);
        localStorage.setItem("storagedUserNamesAll", usernames_all);
    });

    // Show modals when activating/inactivating users
    if (window.location.href.indexOf("activate_users") || window.location.href.indexOf("inactivate_users") || window.location.href.indexOf("delete_users")) {
        var stored = localStorage.getItem("storagedIds");
        var storedUsernames = localStorage.getItem("storagedUserNames");
        var storedUsernamesApproved = localStorage.getItem("storagedUserNamesApproved");
        var storedUsernamesAll = localStorage.getItem("storagedUserNamesAll");
        ids.push(stored)
        usernames_pending.push(storedUsernames)
        usernames_approved.push(storedUsernamesApproved)
        usernames_all.push(storedUsernamesAll)
        let arr_usernames_pending = usernames_pending.toString().split(",")
        let arr_usernames_inact = usernames_approved.toString().split(",")
        let arr_usernames_all = usernames_all.toString().split(",")

        // Add spans for inactive users
        for (let i = 0; i < arr_usernames_pending.length; i++) {
            $("#activate-users-master-div").append("<span class='badge bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis me-2'>" + arr_usernames_pending[i] + "</span>");
        };

        // Add spans for active users
        for (let i = 0; i < arr_usernames_inact.length; i++) {
            $("#inactivate-users-master-div").append("<span class='badge bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis me-2'>" + arr_usernames_inact[i] + "</span>");
        };

        // Add spans for delete users
        for (let i = 0; i < arr_usernames_all.length; i++) {
            $("#delete-users-master-div").append("<span class='badge bg-secondary-subtle border border-secondary-subtle text-secondary-emphasis me-2'>" + arr_usernames_all[i] + "</span>");
        };

        // Show modal for activating users
        if (userId) {
            $('#activate-users').modal('show');
            userId.value = ids
                if (userId.value == '') {
                    document.location.href = '/admin_users';
                };
            localStorage.clear("storagedIds");
            localStorage.clear("storagedUserNames");
        };
        
        // Show modal for deleting users
        if (userIdDel) {
            $('#delete-users').modal('show');
            userIdDel.value = ids
                if (userIdDel.value == '') {
                    document.location.href = '/admin_users';
                };
            localStorage.clear("storagedIds");
            localStorage.clear("storagedUserNamesAll");
        };

        // Show modal for inactivating users
        if (userIdInact) {
            $('#inactivate-users').modal('show');
            userIdInact.value = ids
                if (userIdInact.value == '') {
                    document.location.href = '/admin_users';
                };
            localStorage.clear("storagedIds");
            localStorage.clear("storagedUserNamesApproved");
        };
    };

    // Disable Activate/Inactivate buttons if no boxes are ticked
    // Admin users table 
    if ($('input:checkbox').not(':checked')) {
        $("#activate-modal").addClass('disabled');
        $("#inactivate-modal").addClass('disabled');
        $("#delete-modal").addClass('disabled');

        // Lessons review table / admin finalize
        $('#review-confirm-modal').addClass('disabled');
        $('#review-to-pending-modal').addClass('disabled');
        $('#review-cancel-modal').addClass('disabled');
        $('#fin-finalize-modal').addClass('disabled');
        $('#fin-discard-modal').addClass('disabled');

        $('input:checkbox').change(function() {
            var check_status = $("input:checkbox:checked").closest("tbody").text();
            var checked = $("input:checkbox:checked").length;

            // Activate button
            if (check_status.includes('Pending') && (checked > 0)) {
                $('#activate-modal').removeClass("disabled");
            } else {
              $('#activate-modal').addClass("disabled");
            };

            // Inactivate button
            if (check_status.includes('Approved') && (checked > 0)) {
                $('#inactivate-modal').removeClass("disabled");
            } else {
                $('#inactivate-modal').addClass("disabled");
            };

            // Delete button
            if (check_status.includes('Approved') || check_status.includes('Pending') && (checked > 0)) {
                $('#delete-modal').removeClass("disabled");
            } else {
                $('#delete-modal').addClass("disabled");
            };

            // Confirm button
            if (check_status.includes('Pending') || check_status.includes('Cancelled') && (checked > 0)) {
                $('#review-confirm-modal').removeClass("disabled");
            } else {
                $('#review-confirm-modal').addClass("disabled");
            };

            // To pending button
            if (check_status.includes('Confirmed') || check_status.includes('Cancelled') && (checked > 0)) {
                $('#review-to-pending-modal').removeClass("disabled");
            } else {
                $('#review-to-pending-modal').addClass("disabled");
            };

            // Cancel button
            if (check_status.includes('Confirmed') || check_status.includes('Pending') && (checked > 0)) {
                $('#review-cancel-modal').removeClass("disabled");
            } else {
                $('#review-cancel-modal').addClass("disabled");
            };

            // Finalize button
            if (check_status.includes('Not finalized') && (checked > 0)) {
                $('#fin-finalize-modal').removeClass("disabled");
            } else {
                $('#fin-finalize-modal').addClass("disabled");
            };

            // Discard button
            if (check_status.includes('Not finalized') && (checked > 0)) {
                $('#fin-discard-modal').removeClass("disabled");
            } else {
                $('#fin-discard-modal').addClass("disabled");
            };
        });
    };

    // Disable clear filters button on admin review page
    if ($('#id_confirmed').val() == '' && $('#id_lesson_type').val() == '' && $('#id_date').val() == '') {
        $('#review-clear-filters').addClass("disabled");
    };

    // Disable clear filters button on admin finalize page
    if ($('#id_confirmed').val() == '' && $('#id_lesson_type').val() == '' && $('#datepicker_finalize').val() == '') {
        $('#review-clear-filters').addClass("disabled");
    };

    // Disable search and clear filter buttons on admin archive page
    if ($('#id_student').val() == '' && $('#datepicker_archive').val() == '' && $('#confirmed_archive').val() == '') {
        $('#archive_search').addClass('disabled');
        $('#admin-archive-clear').addClass("disabled");
    };

    // Show Save button when changing lesson status
    var previous_id = [];
    $('.admin-status').change(function() {
        var selected = $(this).attr('label');
        var id = $(this).attr('name');
        var option = $(this).val();
        var save = document.getElementById(selected);
        if (!previous_id.includes(selected)) {
            previous_id.push(selected);
        };

        // Reset dropdown selection if another dropdown is used
        if ($("[id*='admin-status-dd']").is(":visible") == true ) {
            $("[id*='admin-status-dd']").addClass('d-none');
            var element = document.querySelector('[label=' + previous_id[0] + ']').id;
            if (selected != previous_id[0]) {
                $("[id=" + element + "] option:first").prop('selected', true).trigger("change");
            }; 
        };

        $(save).removeClass('d-none');
        if (option == 'Confirmed' || option == 'Pending' || option == 'Cancelled' || option == 'Not finalized') {
            $(save).addClass('d-none');
            previous_id.shift()
        };

        if (option == 'Confirm') {
            option = 'Confirmed'
        } else if (option == 'To pending') {
            option = 'Pending'
        } else if (option == 'Cancel') {
            option = 'Cancelled'
        } else if (option == 'Finalize') {
            option = 'Finalized';
        } else if (option == 'Discard') {
            option = 'Discarded';
        };

        if (reviewStatus) {
            reviewStatus.value = option;
        } else if (finStatus) {
            finStatus.value = option;
        };

        if (reviewId) {
            reviewId.value = id;
        } else if (finId) {
            finId.value = id;
        };

        // Change dropdown colors when changing options
        if (option == 'Confirm' || option == 'Confirmed' || option == 'Finalized') {
            $(this).removeClass('text-warning-emphasis bg-warning-subtle border-warning-subtle text-danger-emphasis bg-danger-subtle border-danger-subtle')
            $(this).addClass('text-success-emphasis bg-success-subtle border-success-subtle')
        } else if (option == 'To pending' || option == 'Pending' || option == 'Not finalized') {
            $(this).removeClass('text-success-emphasis bg-success-subtle border-success-subtle text-danger-emphasis bg-danger-subtle border-danger-subtle')
            $(this).addClass('text-warning-emphasis bg-warning-subtle border-warning-subtle')
        } else if (option == 'Cancel' || option == 'Cancelled' || option == 'Discarded') {
            $(this).removeClass('text-success-emphasis bg-success-subtle border-success-subtle text-warning-emphasis bg-warning-subtle border-warning-subtle')
            $(this).addClass('text-danger-emphasis bg-danger-subtle border-danger-subtle')
        };
    });

    // Confirm lessons modal
    $('#review-confirm-modal, #fin-finalize-modal').on("click", function() {
        $('#user-table').addClass('d-none');
        $('#back-button-admin-users').addClass('d-none');
        if (bulk_confirm) {
            $('#bulk-confirm-modal').modal('show');
            bulk_confirm.value = review_ids
        } else if (bulk_finalize) {
            $('#bulk-finalize-modal').modal('show');
            bulk_finalize.value = review_ids
        };
    });

    // Lessons to pending modal
    $('#review-to-pending-modal').on("click", function() {
        $('#user-table').addClass('d-none');
        $('#back-button-admin-users').addClass('d-none');
        $('#bulk-to-pending-modal').modal('show');
        bulk_to_pending.value = review_ids
    });

    // Cancel lessons modal
    $('#review-cancel-modal, #fin-discard-modal').on("click", function() {
        $('#user-table').addClass('d-none');
        $('#back-button-admin-users').addClass('d-none');
        if (bulk_cancel) {
            $('#bulk-cancel-modal').modal('show');
            bulk_cancel.value = review_ids
        } else if (bulk_discard) {
            $('#bulk-discard-modal').modal('show');
            bulk_discard.value = review_ids
        };
    });

    // Reload admin review page when hiding modal
    $('#bulk-confirm-modal, #bulk-to-pending-modal, #bulk-cancel-modal, #bulk-finalize-modal, #bulk-discard-modal').on('hidden.bs.modal', function () {
        location.reload();
    });

    // Enable search and clear filter buttons on admin archive page
    $('#confirmed_archive, #datepicker_archive').change(function() {
        $('#archive_search').removeClass('disabled');
        $('#admin-archive-clear').removeClass("disabled");
        if (this.value.length === 0 && $('#id_student').val() == '' && $('#confirmed_archive').val() == '' && $('#datepicker_archive').val() == '') {
            $('#archive_search').addClass('disabled');
            $('#admin-archive-clear').addClass("disabled");
        };
    });

    $("#id_student").on("input", function() {
        $('#archive_search').removeClass('disabled');
        $('#admin-archive-clear').removeClass("disabled");
            if (this.value.length === 0 && $('#datepicker_archive').val() == '' && $('#confirmed_archive').val() == '') {
                $('#archive_search').addClass('disabled');
                $('#admin-archive-clear').addClass("disabled");
            };
      });

    $('#archive_search').click(function() {
        localStorage.setItem("reloading", $('#archive-search-wrap'));
    });

    // Display search results on admin archive page
    if (localStorage.getItem("reloading")) {
        $('#archive-search-wrap, #archive-search-title').addClass('d-none');
        if ($('#id_student').val()) {
            $('#archive-search-username').append('<span>Username: <span class="text-success">' + $('#id_student').val() + '</span></span>')
        };
        if ($('#datepicker_archive').val()) {
            $('#archive-search-date').append('<span>Date: <span class="text-success">' + $('#datepicker_archive').val() + '</span></span>')
        };
        if ($('#confirmed_archive').val()) {
            $('#archive-search-confirmed').append('<span>Status: <span class="text-success">' + $('#confirmed_archive').val() + '</span></span>')
        };

        // Show arrows if there are more than 1 search sriteria applied
        if ($('#id_student').val() && $('#datepicker_archive').val()) {
            $('#arrow-1').removeClass('d-none');
        };
        if ($('#datepicker_archive').val() && $('#confirmed_archive').val()) {
            $('#arrow-2').removeClass('d-none');
        };
        if ($('#id_student').val() && $('#confirmed_archive').val()) {
            $('#arrow-1').removeClass('d-none');
        };
        
        $('#archive-new-search-wrap').removeClass('d-none')
    };

    // Clear local storage
    $('#archive-new-search').click(function() {
        localStorage.clear("reloading");
    });

    if (window.location.href.indexOf("admin_archive") == -1) {
        localStorage.clear("reloading");
    };

    // Disable/enable Submit button in Admin notes form
    var comms_form = $("#id_comms").val()
    $("#id_comms").on("input", function() {
        $('#notes_submit').removeAttr('disabled')
        $('#notes_submit').addClass('submit-btn')
        if ($(this).val() == comms_form) {
            $('#notes_submit').attr('disabled', true)
            $('#notes_submit').removeClass('submit-btn')
        };
    });
});

// Swipe function for archive lesson details
var swiper = new Swiper('.swiper-container', {
    slidesPerView: 6,
    touchEventsTarget: 'container',
    paginationClickable: true,
    grabCursor: true,
});