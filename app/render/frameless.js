const { ipcRenderer } = require('electron');

ipcRenderer.on('danmu', (event, nn, txt) => {
    const danmu = document.getElementById('danmu');
    danmu.innerHTML += '<p>' + nn + ':' + txt + '</p>';
    danmu.scrollIntoView(false);
});

$(document).ready(() => {
    $('#wrap').hover(() => {
            $('button').css('display', 'block');
            $('#wrap').css('border', '1px solid');
        }, () => {
            $('button').css('display', 'none');
            $('#wrap').css('border', 'none');
        }
    );
    $('button').click(() => {
        if ($('button').hasClass('lock')) {
            $('body').css('-webkit-app-region', 'no-drag');
            $('button').text('移动').removeClass('lock').addClass('unlock');
        } else if ($('button').hasClass('unlock')) {
            $('body').css('-webkit-app-region', 'drag');
            $('button').text('锁定').removeClass('unlock').addClass('lock');
        }
    });
});
