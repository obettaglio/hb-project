// Adding an exam

function showAddExamForm(evt) {
    // display add-exam-form

    evt.preventDefault();

    $('#add-exam-form').css('visibility', 'visible');
}

function resetAddExamForm(result) {
    // flash success message,
    // clear add-exam-form,
    // update exam-list with result

    console.dir(result);

    $('#flash-msgs').append("<h4 class='msg'>Added exam.</h4>");
    setTimeout(function() {
        $('.msg').remove();
    }, 2000);

    $('#exam-list').append("<p><a href='/classroom/" + result.exam_id + "'>" + result.exam_name + "</a></p>");

    $('#exam-name-field').val('');
    $('#exam-timestamp-field').val('');
    $('#total-points-field').val('');
}

function getExamInfo(evt) {
    // prevent submit button from redirecting,
    // send data to route via post request,
    // call resetAddExamForm

    evt.preventDefault();

    var class_id = $('#class-id').attr('data-class');

    var formInputs = {
        class_id,
        'exam_name': $('#exam-name-field').val(),
        'timestamp': $('#exam-timestamp-field').val(),
        'total_points': $('#total-points-field').val()
    };

    $.post('/classroom/add-exam',  // post route
           formInputs,
           resetAddExamForm
           );
}

$('#add-exam-button').on('click', showAddExamForm);
$('#add-exam-submit').on('click', getExamInfo);