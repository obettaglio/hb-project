// Adding a score to an exam

function showAddScoreForm(evt) {
    // display add-score-form

    evt.preventDefault();

    $('#add-score-form').css('visibility', 'visible');
}

function resetAddScoreForm(result) {
    // flash success message,
    // clear add-score-form,
    // update score-list with result

    console.dir(result);

    $('#flash-msgs').append("<h3 class='msg'>Added score.</h3>");
    setTimeout(function() {
        $('.msg').remove();
    }, 2000);

    $('#score-list').append("<li>Student " + result.student_email + ": " + result.score + "</li>");

    $('#student-email-field').val('');  // clear val() for dropdown?
    $('#score-field').val('');
}

function getScoreInfo(evt) {
    // prevent submit button from redirecting,
    // send data to route via post request,
    // call resetAddScoreForm

    evt.preventDefault();

    var exam_id = $('#exam-id').attr('data-exam');

    var formInputs = {
        exam_id,
        'student_email': $('#student-email-field').val(),
        'score': $('#score-field').val()
    };

    $.post('/classroom/add-score',  // post route
           formInputs,
           resetAddScoreForm
           );
}

$('#add-score-button').on('click', showAddScoreForm);
$('#add-score-submit').on('click', getScoreInfo);