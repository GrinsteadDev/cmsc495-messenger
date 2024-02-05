async function getChatRooms() {
    try {
      const response = await axios.get('/api/chat-rooms');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

async function joinRoom() {
    try {
      const response = await axios.get('/api/join-room');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

async function getOnlineUsers() {
    try {
      const response = await axios.get('/api/online-users');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

async function sendMessage(roomId, userName, message) {
    try {
      const response = await axios.post('/api/send-message', {
        roomId,
        userName,
        message
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

async function peekMessage() {
    try {
      const response = await axios.get('/api/peek-message');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

async function getMessage() {
    try {
      const response = await axios.get('/api/get-message');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

async function createRoom(roomName, userName) {
    try {
      const response = await axios.post('/api/create-room', {
        roomName,
        userName
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

async function deleteRoom(roomId) {
    try {
      const response = await axios.post('/api/delete-room', {
        roomId
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}