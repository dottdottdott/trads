document.addEventListener('DOMContentLoaded', function() {

    // Submit new Message
    document.getElementById('send-message').addEventListener('click', function(event) {
            event.preventDefault();
            sendMessage();
        });

});

function fetch_call(url, method, data, success=()=>null, error=null, ctype=null) {
    const errorfunc = () => {
        if (typeof error === "function") {
            error();
        } else {
            console.error('Error:', error);
        }
    }   
    let fetch_data = {method: method, body: data};
    if (ctype == "json"){
        fetch_data.headers = {"Content-Type": "application/json",};
        if ( method != "GET" ) {
            fetch_data.body = JSON.stringify(data);
        }
    }
    fetch(url, fetch_data )
        .then(res => {
            return res.json();
        })
        .then(res => {
            success(res);
        })
        .catch(error => {
            errorfunc();
        });
};

function sendMessage() {
    const msg = document.getElementById('new-message').value;
    const url = document.getElementById('chatblock').getAttribute('data-url');
    const oname = document.getElementById('chatblock').getAttribute('data-men');
    const photo = document.getElementById('chatblock').getAttribute('data-mep');
    
    const data = new FormData();
    data.append('content', msg);
    data.append('correspondant', url);

    const successfunc = result => {
        const html = `<div class="chat-message">
        <img class="user-avatar" src="${ photo }" alt="${ oname }">
        <div class="chat-user">${oname}</div>
        <div class="chat-text">${msg}</div>
        </div>`
        const postdiv = document.getElementById('chatblock');
        postdiv.insertAdjacentHTML('beforeend', html)
        document.getElementById('new-message').value = "";
    }

    fetch_call(MESSAGES_URL, "POST", data, successfunc, null);
};

