/*
Purpose:
   Chat
   Client side functionality for chatting between users within rooms

Contributors:
   Michael Gurewitz
   Devin Grinstead
   
*/

const axios = window.axios;

export async function getChatRooms() {
    try {
      const response = await axios.get('/api/chat-rooms');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

export async function joinRoom() {
    try {
      const response = await axios.get('/api/join-room');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

export async function getOnlineUsers() {
    try {
      const response = await axios.get('/api/online-users');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

export async function sendMessage(roomId, userName, message) {
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

document.addEventListener('DOMContentLoaded', (event) => {
  const sendMessageForm = document.getElementById('sendMessageForm');
  if (sendMessageForm) {
    sendMessageForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(sendMessageForm);
      const roomId = formData.get('roomId');
      const userName = formData.get('userName');
      const message = formData.get('message');
      await sendMessage(roomId, userName, message);
      document.getElementById('message').value = '';
    });
  }
});

export async function peekMessage() {
    try {
      const response = await axios.get('/api/peek-message');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

export async function getMessage() {
    try {
      const response = await axios.get('/api/get-message');
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

export async function createRoom(roomName, userName) {
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

document.addEventListener('DOMContentLoaded', (event) => {
  const createRoomForm = document.getElementById('createRoomForm');
  if (createRoomForm) {
    createRoomForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(createRoomForm);
      const roomName = formData.get('roomName');
      const userName = formData.get('userName');
      await createRoom(roomName, userName);
    });
  }
});

export async function deleteRoom(roomId) {
    try {
      const response = await axios.post('/api/delete-room', {
        roomId
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
  const deleteRoomButton = document.getElementById('deleteRoomButton');
  if (deleteRoomButton) {
    deleteRoomButton.addEventListener('click', async (e) => {
      e.preventDefault();
      const roomId = deleteRoomButton.getAttribute('data-room-id');
      await deleteRoom(roomId);
    });
  }
});