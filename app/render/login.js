// 设置房间号
function setRoomId() {
    var roomid = document.getElementById('roomid').value;
    const { ipcRenderer } = require('electron');
    ipcRenderer.send('login', roomid);
}
// github链接
$(document).ready(function() {
    // 回车登录
    $('#roomid').keypress(function(event) {
        if (event.which == 13) {
            setRoomId();
        }
    });

    const roomBtn = document.getElementById('room-btn');
    roomBtn.addEventListener('click', (event) => {
        setRoomId();
    });
});
