// Adding a student to the roster

function showAddStudentToRosterForm(evt) {
    // display add-student-to-roster-form

    evt.preventDefault();

    $('#add-student-to-roster-form').css('visibility', 'visible');
}

function resetAddStudentToRosterForm(result) {
    // flash success message,
    // clear add-student-form,
    // update student-roster-table with result

    console.dir(result);

    $('#flash-msgs').append("<h3 class='msg'>Added student.</h3>");
    setTimeout(function() {
        $('.msg').remove();
    }, 2000);

    $('#student-roster-table').append("<tr> \
      <td>" + result.full_name + "</td> \
      <td>" + result.student_email + "</td> \
      <td>" + result.khan_username + "</td> \
    </tr>");

    $('#f-name-field').val('');
    $('#l-name-field').val('');
    $('#student-email-field').val('');
    $('#khan-username-field').val('');

    // location.reload();
}

function getStudentInfo(evt) {
    // prevent submit button from redirecting,
    // send data to route via post request,
    // call resetAddStudentToRosterForm

    evt.preventDefault();

    var formInputs = {
        'f_name': $('#f-name-field').val(),
        'l_name': $('#l-name-field').val(),
        'student_email': $('#student-email-field').val(),
        'khan_username': $('#khan-username-field').val()
    };

    $.post('/classroom/add-student',  // post route
           formInputs,
           resetAddStudentToRosterForm
           );
}

$('#add-student-to-roster-button').on('click', showAddStudentToRosterForm);
$('#add-student-to-roster-submit').on('click', getStudentInfo);