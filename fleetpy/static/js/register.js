document.addEventListener('DOMContentLoaded', function () {
    var registerForm = document.getElementById('register-form');

    registerForm.addEventListener('submit', function (event) {
        var isValid = true;

        // Username validation
        var username = document.getElementById('username');
        var usernameError = document.getElementById('username-error');
        if (!/^[\w.@+-]+$/.test(username.value) || username.value.length > 150) {
            usernameError.style.display = 'block';
            isValid = false;
        } else {
            usernameError.style.display = 'none';
        }

        // Email validation
        var email = document.getElementById('email');
        var emailError = document.getElementById('email-error');
        if (!/\S+@\S+\.\S+/.test(email.value)) {
            emailError.style.display = 'block';
            isValid = false;
        } else {
            emailError.style.display = 'none';
        }

        // Password validation
        var password = document.getElementById('password');
        var passwordError = document.getElementById('password-error');
        if (password.value.length < 8 || /^\d+$/.test(password.value) || password.value.toLowerCase() === username.value.toLowerCase() || /password/.test(password.value.toLowerCase())) {
            passwordError.style.display = 'block';
            isValid = false;
        } else {
            passwordError.style.display = 'none';
        }

        // Password confirmation validation
        var password2 = document.getElementById('password2');
        var password2Error = document.getElementById('password2-error');
        if (password.value !== password2.value) {
            password2Error.style.display = 'block';
            isValid = false;
        } else {
            password2Error.style.display = 'none';
        }

        // Password authentication validation
        var passwordAuth = document.getElementById('password_auth');
        var passwordAuthError = document.getElementById('password-auth-error');
        if (passwordAuth.value === '') {
            passwordAuthError.style.display = 'block';
            isValid = false;
        } else {
            passwordAuthError.style.display = 'none';
        }

        if (!isValid) {
            event.preventDefault();
        }
    });
});