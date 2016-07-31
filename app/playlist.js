const { shell, ipcRenderer } = require('electron');

$(document).ready(function() {
    const githubLink = document.getElementById('github');
    githubLink.addEventListener('click', function(event) {
        shell.openExternal('http://github.com/zephyrzoom');
    });

    ipcRenderer.send('getList');
});

ipcRenderer.on('playlist', (event, arg) => {
    const playlist = document.getElementById('playlist');
    playlist.innerHTML = '';
    for (let i in arg) {
        playlist.innerHTML += '<tr><td>' + (Number(i) + 1) + '. ' + arg[i][0] + '</td></tr>';
    }
});
