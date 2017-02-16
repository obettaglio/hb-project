// Adding an exam

function showAddScoreForm(result) {
    // display add-score-form

    console.dir(result);

    $('#add-score-form').css('visibility', 'visible');
}

function resetAddScoreForm() {
    // flash success message,
    // clear add-score-form
}

function getScoreInfo(evt) {
    // prevent submit button from redirecting,
    // send data to route via post request,
    // call showAddScoreForm

    evt.preventDefault();

    var formInputs = {
        "student-email": $("#student-email-field").val(),
        "score": $("#score-field").val()
    };

    $.post("/add-score",  // post route
           formInputs,
           resetAddScoreForm
           );
}

$('#add-score-button').on('click', showAddScoreForm);
$('#add-score-submit').on('click', getScoreInfo)