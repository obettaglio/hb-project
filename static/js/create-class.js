// Creating a class and student roster

function showAddStudentToNewClassForm(result) {
    // flash success message,
    // disable create-class-submit,
    // display add-student-header and add-student-form

    console.dir(result);

    $('#flash-msgs').append("<h4 class='msg'>Created class.</h4>");
    setTimeout(function() {
        $('.msg').remove();
    }, 2000);

    $('#create-class-submit').css('visibility', 'hidden');
    $('#add-student-to-new-class-header').css('visibility', 'visible');
    $('#add-student-to-new-class-form').css('visibility', 'visible');
}

function getClassInfo(evt) {
    // prevent submit button from redirecting,
    // send data to route via post request,
    // call showAddStudentToNewClassForm

    evt.preventDefault();

    var formInputs = {
        "class_name": $("#class-name-field").val(),
        "subject": $("#subject-field").val()
    };

    $.post("/create-class",  // post route
           formInputs,
           showAddStudentToNewClassForm
           );
}

function resetAddStudentToNewClassForm(result) {
    // flash success message,
    // clear add-student-form

    console.dir(result);
    $('#flash-msgs').append("<h4 class='msg'>Added student.</h4>");
    setTimeout(function() {
        $('.msg').remove();
    }, 2000);

    $('#complete-class').show();

    $('#f-name-field').val('');
    $('#l-name-field').val('');
    $('#student-email-field').val('');
    $('#khan-username-field').val('');
}

function getStudentInfo(evt) {
    // prevent submit button from redirecting,
    // send data to route via post request,
    // call resetAddStudentToNewClassForm

    evt.preventDefault();

    var formInputs = {
        "f_name": $("#f-name-field").val(),
        "l_name": $("#l-name-field").val(),
        "student_email": $("#student-email-field").val(),
        "khan_username": $("#khan-username-field").val()
    };

    $.post("/classroom/add-student",  // post route
           formInputs,
           resetAddStudentToNewClassForm
           );
}


$('#create-class-submit').on('click', getClassInfo);
$('#add-student-to-new-class-submit').on('click', getStudentInfo);