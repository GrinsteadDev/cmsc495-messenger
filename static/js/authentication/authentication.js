const axios = window.axios;

async function registerUser(firstName, lastName, userName, userEmail, userPassword){
  try {
    const response = await axios.post('/api/register', {
      firstName,
      lastName,
      userName,
      userEmail,
      userPassword
    });
    console.log(response.data);
    } catch (error) {
    console.error(error);
  }
}

document.addEventListener('DOMContentLoaded', (event) => {
  const form = document.getElementById('registerUserForm');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const firstName = formData.get('firstName');
      const lastName = formData.get('lastName');
      const userName = formData.get('userName');
      const userEmail = formData.get('userEmail');
      const userPassword = formData.get('userPassword');
      await registerUser(firstName, lastName, userName, userEmail, userPassword);
    });
  }
});

async function login(userName, password, status = 'active') {
  try {
    const response = await axios.post('/api/login', {
      username: userName,
      password,
      status
    });
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener('DOMContentLoaded', (event) => {
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      const userName = formData.get('userName');
      const password = formData.get('password');
      await login(userName, password);
    });
  }
});

async function logout(logoutMessage = '') {
  try {
    const token = 'ACCESS_TOKEN'; //TODO: Put real value here
    const response = await axios.post('/api/logout', {
      message: logoutMessage
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener('DOMContentLoaded', (event) => {
  const logoutButton = document.getElementById('logoutButton');
  if (logoutButton) {
    logoutButton.addEventListener('click', async (e) => {
      e.preventDefault();
      await logout();
    });
  }
});

async function passwordRecovery(userEmail) {
  try {
    const response = await axios.post('/api/password-recovery', {
      email: userEmail
    });
    console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
  const passwordRecoveryForm = document.getElementById('passwordRecoveryForm');
  if (passwordRecoveryForm) {
    passwordRecoveryForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(passwordRecoveryForm);
      const userEmail = formData.get('userEmail');
      await passwordRecovery(userEmail);
    });
  }
});