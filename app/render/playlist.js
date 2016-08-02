const { shell, ipcRenderer } = require('electron');

$(document).ready(function() {
    ipcRenderer.send('getList');
});

ipcRenderer.on('playlist', (event, arg) => {
    const playlist = document.getElementById('playlist');
    playlist.innerHTML = '';
    for (let i in arg) {
        playlist.innerHTML += '<tr><td>' + (Number(i) + 1) + '. ' + arg[i][0] + '</td></tr>';
    }
});
