// Adding a score to an exam
// Changing chart display according to user command

function removeLoadingGif() {
    // remove curtain div,
    // show chart div

    setTimeout(function() {
        $('#curtain').hide();
        $('#chart-container').show();
    }, 3000);
}

removeLoadingGif()

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

    $('#added-score-flash').append("<p class='msg'><br>Added score.</h4>");
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

    $('#chartdiv').load(document.URL +  ' #chartdiv');
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

function changeChartDisplay(evt, this_panel, that_panel, chart, chart_title) {
    // prevent button from redirecting,
    // hide all charts,
    // show desired chart

    evt.preventDefault();

    this_panel.attr("class", "active")
    that_panel.removeAttr("class")

    $('.exam-chart').hide();
    chart.show();
    $('.exam-chart-title').hide();
    chart_title.show();
}

$('#add-score-button').on('click', showAddScoreForm);
$('#add-score-submit').on('click', getScoreInfo);

// $('#bar-button').on('click', function(evt) {changeChartDisplay(evt, $('#bar-chart'), $('#bar-chart-title'))});
// $('#scatterplot-button').on('click', function(evt) {changeChartDisplay(evt, $('#timestamp-chart'), $('#timestamp-chart-title'))});

$('#bar-panel').on('click', function(evt) {changeChartDisplay(evt, $('#bar-panel'), $('#timestamp-panel'), $('#bar-chart'), $('#bar-chart-title'))});
$('#timestamp-panel').on('click', function(evt) {changeChartDisplay(evt, $('#timestamp-panel'), $('#bar-panel'), $('#timestamp-chart'), $('#timestamp-chart-title'))});