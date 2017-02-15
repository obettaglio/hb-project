// Adding a new class and student roster

function addClass(results) {
    // add class via AJAX request,
    // display add-student-form  >> TO DO <<

    console.dir(results);
    alert('Successfully added new class.');
    $('add-class-submit').attr('hidden', true);
    $('add-student-to-new-class-form').attr('hidden', false);
}

function getClassInfo(evt) {
    // prevent submit button from redirecting,
    // get data from JSON,  >> TO DO <<
    // call callbackFunction

    evt.preventDefault();

    var formInputs = {
        "class-name": $("#class-name-field").val(),
        "subject": $("#subject-field").val()
    };

    $.get("/student-info.json",  // results
          formInputs,
          addClass);
}

$('#add-class-form').on('submit', getClassInfo);