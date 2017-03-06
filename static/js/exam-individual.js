// Adding a score to an exam
// Changing chart display according to user command

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

    $('#flash-msgs').append("<h4 class='msg'>Added score.</h4>");
    setTimeout(function() {
        $('.msg').remove();
    }, 2000);

    $('#no-scores').hide();

    $('#scores-table').append("<tr> \
      <td>" + result.student_name + "</td> \
      <td>" + result.score + "</td> \
    </tr>");

    $('#student-email-field').val('');  // clear val() for dropdown?
    $('#score-field').val('');

    $('#exam-chart-div').load(document.URL +  ' #exam-chart-div');
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

function changeChartDisplay(evt, chart, chart_title) {
    // prevent button from redirecting,
    // hide all charts,
    // show desired chart

    evt.preventDefault();

    $('.exam-chart').hide();
    chart.show();
    $('.exam-chart-title').hide();
    chart_title.show();
}

$('#add-score-button').on('click', showAddScoreForm);
$('#add-score-submit').on('click', getScoreInfo);

$('#bar-button').on('click', function(evt) {changeChartDisplay(evt, $('#bar-chart'), $('#bar-chart-title'))});
// $('#pie-button').on('click', function(evt) {changeChartDisplay(evt, $('#pie-chart'))});
$('#scatterplot-button').on('click', function(evt) {changeChartDisplay(evt, $('#timestamp-chart'), $('#timestamp-chart-title'))});