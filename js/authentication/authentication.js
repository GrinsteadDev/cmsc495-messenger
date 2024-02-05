import axios from 'axios';

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