$(document).ready(function () {
    function showMessage(message) {
        let messageElem = $('#main');
        messageElem.html(message.data);
    }

    let ws = new WebSocket(WS_URL);
    console.log(ws);

    ws.onmessage = (message) => {
        console.log(message);
        showMessage(message);
    }

    ws.onclose = (event) => {
        if (event.wasClean) {
            showMessage("Clean connection end")
        } else {
            showMessage("Connection broken")
        }
    };

    ws.onerror = (error) => showMessage(error);

});