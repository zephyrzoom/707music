const config = require('../util/config');

const { ipcRenderer } = require('electron');

let cfg;
$(document).ready(() => {
    config.getConfig((data) => {
        cfg = data;
        if (data.music == 'true') {
            $('#music').addClass('btn-negative').text('关闭点歌');
        } else {
            $('#music').addClass('btn-positive').text('开启点歌');
        }
        if (data.desktopDanmu == 'true') {
            $('#desktopDanmu').addClass('btn-negative').text('关闭弹幕');
        } else {
            $('#desktopDanmu').addClass('btn-positive').text('开启弹幕');
        }
    });

    $('#music').click(() => {
        if ($('#music').hasClass('btn-negative')) {
            cfg.music = 'false';
            $('#music').removeClass('btn-negative').addClass('btn-positive').text('开启点歌');
        } else {
            cfg.music = 'true';
            $('#music').removeClass('btn-positive').addClass('btn-negative').text('关闭点歌');
        }
        ipcRenderer.send('update-config', cfg);
        config.setConfig(cfg);
    });

    $('#desktopDanmu').click(() => {
        if ($('#desktopDanmu').hasClass('btn-negative')) {
            cfg.desktopDanmu = 'false';
            $('#desktopDanmu').removeClass('btn-negative').addClass('btn-positive').text('开启弹幕');
        } else {
            cfg.desktopDanmu = 'true';
            $('#desktopDanmu').removeClass('btn-positive').addClass('btn-negative').text('关闭弹幕');
        }
        ipcRenderer.send('update-config', cfg);
        config.setConfig(cfg);
    });
});
