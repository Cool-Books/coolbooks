const slidePage = document.querySelector(".slide-page");
const nextBtnFirst = document.querySelector(".firstNext");
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
const prevBtnThird = document.querySelector(".prev-2");
const nextBtnThird = document.querySelector(".next-2");
const prevBtnFourth = document.querySelector(".prev-3");
const submitBtn = document.querySelector(".submit");
const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");
let current = 1;

nextBtnFirst.addEventListener("click", function (event) {
  event.preventDefault();
  slidePage.style.marginLeft = "-25%";
  bullet[current - 1].classList.add("active");
  progressCheck[current - 1].classList.add("active");
  progressText[current - 1].classList.add("active");
  current += 1;
});
nextBtnSec.addEventListener("click", function (event) {
  event.preventDefault();
  slidePage.style.marginLeft = "-50%";
  bullet[current - 1].classList.add("active");
  progressCheck[current - 1].classList.add("active");
  progressText[current - 1].classList.add("active");
  current += 1;
});
nextBtnThird.addEventListener("click", function (event) {
  event.preventDefault();
  slidePage.style.marginLeft = "-75%";
  bullet[current - 1].classList.add("active");
  progressCheck[current - 1].classList.add("active");
  progressText[current - 1].classList.add("active");
  current += 1;
});

// Collect form data
const bio = document.getElementById('bio-input');
const firstName = document.getElementById('first_name');
const lastName = document.getElementById('last_name');
const gender = document.getElementById('gender');
const userName = document.getElementById('user_name');
const otherNames = document.getElementById('other_names');
const email = document.getElementById('email');
const password = document.getElementById('pwd-field');
const confirmPass = document.getElementById('password_confirm');

//check the validity of password
password.addEventListener('input', checkPassword);


// check if password match
confirmPass.addEventListener('input', function () {
  const match = document.querySelector('.match')
  match.textContent = ''
  const getPassword = password.value.trim()
  const getConfirmPass = confirmPass.value.trim()

  if (getPassword !== getConfirmPass) {
    match.innerHTML = '<b>Password not match!</b>'
  } else {
    match.textContent = ''
  }
})

submitBtn.addEventListener("click", function (event) {
  event.preventDefault(); // Prevent default form submission behavior

  const formData = {
    bio: bio.value,
    first_name: firstName.value.trim(),
    last_name: lastName.value.trim(),
    email: email.value.trim(),
    password: password.value.trim(),
    other_names: otherNames.value.trim(),
    user_name: userName.value.trim(),
    gender: gender.value.trim(),
    password_confirm: confirmPass.value.trim(),
  };

  // Send the POST request to the signup endpoint
  fetch("http://localhost:5000/coolbooks/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(formData) // Send form data as dict
  })
    .then(response => {
      return response.json().then(data => {
        if (response.status === 200) {
          bullet[3].classList.add("active"); // Show step 4 bullet as active
          progressCheck[3].classList.add("active"); // Show step 4 checkmark
          progressText[3].classList.add("active"); // Show step 4 text
          alert(data.success);
          location.reload();
        } else {
          alert(data.Error);
        }
      });
    })
    .catch(error => {
      alert("An error occurred. Please try again.");
    });
});

prevBtnSec.addEventListener("click", function (event) {
  event.preventDefault();
  slidePage.style.marginLeft = "0%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});
prevBtnThird.addEventListener("click", function (event) {
  event.preventDefault();
  slidePage.style.marginLeft = "-25%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});
prevBtnFourth.addEventListener("click", function (event) {
  event.preventDefault();
  slidePage.style.marginLeft = "-50%";
  bullet[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  current -= 1;
});

const bioInput = document.getElementById("bio-input");
const charCount = document.getElementById("char-count");
const maxLength = 250;

bioInput.addEventListener("input", function () {
  const remaining = maxLength - bioInput.value.length;
  charCount.innerHTML = `<b>${remaining} characters remaining</b>`;
});


function checkPassword() {
  const checkPwd = password.value.trim()
  const pwdReq = document.getElementById('pwd-req');
  pwdReq.style.color = 'red';

  let errors = []; // Collect all the password requirement errors here

  if (checkPwd.length < 8) {
    errors.push("Password must be at least 8 characters");
  }
  if (!/[A-Z]/.test(checkPwd)) {
    errors.push("Password must contain at least one uppercase letter");
  }
  if (!/[0-9]/.test(checkPwd)) {
    errors.push("Password must contain at least one number");
  }
  if (!/[!@#$%^&*(),.?\":{}|<>]/.test(checkPwd)) {
    errors.push("Password must contain at least one special character");
  }

  // If there are errors, display them; otherwise, show success
  if (errors.length > 0) {
    pwdReq.innerHTML = `<b>${errors.join("<br>")}</b>`; // Display all errors
  } else {
    pwdReq.style.color = 'green'; // Change color for success
    pwdReq.innerHTML = '<b>Password meets all requirements!</b>';
  }

}