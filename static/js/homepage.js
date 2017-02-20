// Display register and login forms

function showRegisterOnHomepage(evt) {
    // display register-on-homepage

    evt.preventDefault();

    $('.register-on-homepage').css('visibility', 'visible');
}

function showLoginOnHomepage(evt) {
    // display login-on-homepage

    evt.preventDefault();

    $('.login-on-homepage').css('visibility', 'visible');
}

function resetAddExamForm(result) {
    // flash success message,
    // clear add-exam-form,
    // update exam-list with result

    console.dir(result);

    $('#flash-msgs').append("<h3 class='msg'>Added exam.</h3>");
    setTimeout(function() {
        $('.msg').remove();
    }, 2000);

    $('#exam-list').append("<p><a href='/classroom/" + result.exam_id + "'>" + result.exam_name + "</a></p>");

    $('#exam-name-field').val('');
    $('#total-points-field').val('');
}

function getExamInfo(evt) {
    // prevent submit button from redirecting,
    // send data to route via post request,
    // call resetAddExamForm

    evt.preventDefault();

    var exam_id = $('#exam-id').attr('data-exam');

    var formInputs = {
        exam_id,
        'exam_name': $('#exam-name-field').val(),
        'total_points': $('#total-points-field').val()
    };

    $.post('/classroom/add-exam',  // post route
           formInputs,
           resetAddExamForm
           );
}

$('#register-on-homepage-button').on('click', showRegisterOnHomepage);
$('#login-on-homepage-button').on('click', showLoginOnHomepage);