const { shell } = require('electron');

$(document).ready(function() {
    const githubLink = document.getElementById('github');
    githubLink.addEventListener('click', function(event) {
        shell.openExternal('http://github.com/zephyrzoom');
    });
});
