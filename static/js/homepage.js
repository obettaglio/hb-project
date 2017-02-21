// Display register and login forms

function showRegisterOnHomepage(evt) {
    // display register-on-homepage

    evt.preventDefault();

    $('.register-on-homepage').css('visibility', 'visible');
}

function showLoginOnHomepage(evt) {
    // display login-on-homepage

    evt.preventDefault();

    $('.login-on-homepage').css('visibility', 'visible');
}

$('#register-on-homepage-button').on('click', showRegisterOnHomepage);
$('#login-on-homepage-button').on('click', showLoginOnHomepage);