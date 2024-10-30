const resetBtn = document.querySelector('#reset-btn');

resetBtn.addEventListener('click', function(event) {
    event.preventDefault();
    const email = document.getElementById('email');
    const formData = { "email": email.value.trim() }
    
    fetch('http://localhost:5000/coolbooks/forgot_pwd', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
     .then((response) => {
         return response.json().then(data => {
             if (response.status === 200) {
                 alert(data.success);
                 location.reload();
             } else {
                 alert(data.Error);
             }
         }).catch(err => {
             toastr.error('Error sending reset link');
         });
     });
});
