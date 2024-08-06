document.getElementById('register-form').addEventListener('submit', function (e) {
  e.preventDefault();
  registerUser();
});

function registerUser() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const age = document.getElementById('age').value;

  fetch('http://localhost:8080/users', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, email, password, age })
  })
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok ' + response.statusText);
          }
          return response.json();
      })
      .then(user => {
          alert('User registered successfully!');
          window.location.href = 'login.html';
      })
      .catch(error => console.error('Error registering user:', error));
}
