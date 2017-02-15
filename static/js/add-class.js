// Adding a new class and student roster

function addClass(results) {
    console.dir(results); // yay debugging!
    alert('Successfully added new class.');
    $('add-class-submit').attr('hidden', true);
    $('add-student-to-new-class-form').attr('hidden', false);
}

function getClassInfo(evt) {
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