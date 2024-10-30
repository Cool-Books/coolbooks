const password = document.getElementById('new_password');
const password_confirm = document.getElementById('new_password_confirm');

password.addEventListener('input', checkPwd)

password_confirm.addEventListener('input', () => {
    const match = document.querySelector('.match')
    match.innerHTML = '';
    if (password.value.trim() != password_confirm.value.trim()) {
        match.innerHTML = 'password not match!'
        match.style.color = 'red';
    } else {
        match.innerHTML = '';
    }
})

function getTokenFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('token');
}

document.addEventListener('DOMContentLoaded', function () {
    const token = getTokenFromUrl();
    if (token) {
        document.getElementById('token').value = token;
    }
});

// Attach the event listener to the form, not the button
document.getElementById('reset-password-form').addEventListener('submit', function (event) {
    event.preventDefault();

    // Extract the data
    const token = document.getElementById('token').value; // get the token from the hidden input

    const formData = {
        new_password: password.value.trim(),
        new_password_confirm: password_confirm.value.trim(),
        token: token
    };

    fetch('http://localhost:5000/coolbooks/reset_pwd', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
     .then((response) => {
        return response.json()
         .then(data => {
            if (response.status === 200) {
                alert(data.success)
            } else {
                alert(data.Error)
            }
         }).catch(err => alert(err))
     });
});

function checkPwd() {
    let errors = [];
    const pwdReq = document.getElementById('pwd-req')
    pwdReq.style.color = 'red'
    const getPwd = password.value.trim()
    if (getPwd.length < 8) {
        errors.push("Password must be at least 8 characters");
    }
    if (!/[A-Z]/.test(getPwd)) {
        errors.push("Password must contain at least one uppercase letter");
    }
    if (!/[0-9]/.test(getPwd)) {
        errors.push("Password must contain at least one number");
    }
    if (!/[!@#$%^&*(),.?\":{}|<>]/.test(getPwd)) {
        errors.push("Password must contain at least one special character");
    }
    if (errors.length > 0) {
        pwdReq.innerHTML = `<b>${errors.join("<br>")}</b>`;
    } else {
        pwdReq.style.color = 'green'; // Change color for success
        pwdReq.innerHTML = '<b>Password meets all requirements!</b>';
    }
}