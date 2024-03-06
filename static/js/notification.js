function showNotification(title, body, timeout) {
    let nElm = document.querySelector('#notification');
    let nTitle = nElm.querySelector('#notification-title');
    let nBody = nElm.querySelector('#notification-body');

    nTitle.textContent = title;
    nBody.innerHTML = body;

    nElm.classList.remove('hidden');

    setTimeout(
        ()=>{
            nElm.classList.add('hidden');
        },
        timeout || 2000
    )
}