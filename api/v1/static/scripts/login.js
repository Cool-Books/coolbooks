const submitBtn = document.querySelector("#log-in")

submitBtn.addEventListener('click', function (event) {
    event.preventDefault(); // prevent default submission behavior

    // collect login data
    const email = document.getElementById('email');
    const password = document.getElementById('pwd');

    const formData = {
        email: email.value.trim(),
        password: password.value.trim(),
    }
    console.log(formData);

    // make post request
    fetch('http://localhost:5000/coolbooks/login', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formData) //send as json
    })
        .then((response) => {
            return response.json().then(data => {
                if (response.status === 200) {
                    alert(data.success);
                    location.reload();
                } else {
                    return alert(data.Error);
                }
            }).catch(err => { return err; });
        });
});
