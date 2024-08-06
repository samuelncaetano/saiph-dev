document.getElementById('login-form').addEventListener('submit', function (e) {
  e.preventDefault();
  console.log('Login form submitted');
  loginUser();
});

function loginUser() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  console.log(`Attempting login with email: ${email}`);

  fetch('http://localhost:8080/users/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
  })
      .then(response => {
          console.log('Received response from server');
          if (!response.ok) {
              console.error('Network response was not ok', response.statusText);
              throw new Error('Network response was not ok ' + response.statusText);
          }
          return response.json();
      })
      .then(user => {
          console.log('User logged in successfully', user);
          setUser(user);  // Certifique-se de que setUser está definido corretamente
          window.location.href = 'dashboard.html';
      })
      .catch(error => console.error('Error logging in:', error));
}
