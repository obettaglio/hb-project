// Display register and login forms

function showRegisterOnHomepage(evt) {
    // display register-on-homepage

    evt.preventDefault();

    $('.register-on-homepage').css('visibility', 'visible');
}

function showLoginOnHomepage(evt) {
    // display login-on-homepage

    evt.preventDefault();
    // $('.login-container').html($('.login-on-homepage').clone());
    // $('.login-on-homepage').show()
    $('.login-on-homepage').css('visibility', 'visible');
}

function changeSignInDisplay(evt, div) {
    // hide all forms,
    // show desired form

    evt.delay(function (div) {$('.sign-in-div').hide();
                           div.show();}
    );

    // $('.sign-in-div').hide();
    // div.show();
}

$('#register-on-homepage-button').on('click', showRegisterOnHomepage);
$('#login-on-homepage-button').on('click', showLoginOnHomepage);

$('#register-nav-button').on('click', function(evt) {changeSignInDisplay(evt, $('#register-div'));});
$('#login-nav-button').on('click', function(evt) {changeSignInDisplay(evt, $('#login-div'));});