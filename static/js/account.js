const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

// const SingUp = document.getElementById("SignUp");
// const SignIn = document.getElementById("SignIn");


// signUpButton.addEventListener('click', () => {
//   container.classList.add("right-panel-active");
// });

signUpButton.addEventListener('click', () => {
    location.href = "http://127.0.0.1:8000/login/signup";
});

signInButton.addEventListener('click', () => {
  container.classList.remove("right-panel-active");
});


