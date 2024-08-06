document.addEventListener('DOMContentLoaded', function () {
  console.log('Dashboard loaded');
  loadUserInfo();
});

function loadUserInfo() {
  const user = getUser();
  console.log('Loaded user from localStorage', user);

  if (!user) {
      console.log('No user found, redirecting to login');
      logout();
      return;
  }

  const userInfo = document.getElementById('user-info');
  userInfo.innerHTML = `Name: ${user.name}, Email: ${user.email}, Age: ${user.age}`;
}
