// Adding a student to the roster

function showAddStudentForm(evt) {
    // display add-student-form

    evt.preventDefault();

    $('#add-student-form').css('visibility', 'visible');
}

function resetAddStudentForm(result) {
    // flash success message,
    // clear add-student-form

    console.dir(result);
}

function getStudentInfo(evt) {
    // prevent submit button from redirecting,
    // send data to route via post request,
    // call resetAddStudentForm

    // REDO //

    evt.preventDefault();

    var exam_id = $('#exam-id').attr('data-exam');

    var formInputs = {
        exam_id,
        'student_email': $('#student-email-field').val(),
        'score': $('#score-field').val()
    };

    $.post('/classroom/add-student',  // post route
           formInputs,
           resetAddStudentForm
           );
}

$('#add-student-button').on('click', showAddStudentForm);
$('#add-student-submit').on('click', getStudentInfo)