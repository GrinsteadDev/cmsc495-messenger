function fetchMessages() {
    fetch('/api/peek-message')
        .then(response => response.json())
        .then(data => {
            postMessage(data);
        })
        .catch(error => console.error('Error fetching messages:', error));
}

// setInterval(fetchMessages, 1000);
self.addEventListener('message', (event) => {
    console.log('Message:',event.data);
});

/*

TODO: Place this where we want the worker to begin being loaded

if (window.Worker) {
    const messageWorker = new Worker('static/js/required/messageWorker.js');
    messageWorker.onmessage = function(event) {
        console.log('New message:', event.data);
    };
} else {
    console.log('Your browser does not support web workers.');
}


*/
