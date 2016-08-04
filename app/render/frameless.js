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
        $('select').css('display', 'block');
    }, () => {
        $('button').css('display', 'none');
        $('#wrap').css('border', 'none');
        $('select').css('display', 'none');
    });

    $('button').click(() => {
        if ($('button').hasClass('lock')) {
            $('body').css('-webkit-app-region', 'no-drag');
            $('button').text('移动').removeClass('lock').addClass('unlock');
        } else if ($('button').hasClass('unlock')) {
            $('body').css('-webkit-app-region', 'drag');
            $('button').text('锁定').removeClass('unlock').addClass('lock');
        }
    });

    $('select').change(() => {
        const color = $('select option:selected').text();
        switch (color) {
            case '红':
                $('#danmu').css('color', 'red');
                break;
            case '黑':
                $('#danmu').css('color', 'black');
                break;
            case '黄':
                $('#danmu').css('color', 'yellow');
                break;
            case '绿':
                $('#danmu').css('color', 'green');
                break;
            case '蓝':
                $('#danmu').css('color', 'blue');
                break;
            case '白':
                $('#danmu').css('color', 'white');
                break;
            case '灰':
                $('#danmu').css('color', 'gray');
                break;
            case '棕':
                $('#danmu').css('color', 'brown');
                break;
            case '紫':
                $('#danmu').css('color', 'purple');
                break;
            default:
        }
    });
});
