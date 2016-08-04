const electron = require('electron');
const { shell, ipcRenderer } = electron;
const { BrowserWindow, ipcMain } = electron.remote;

const diange = require('../player/system');
const danmu = require('../danmu/danmu');
const config = require('../util/config');

let cfg;
let desktopDanmuWin = null;
let settingsWin = null;
let playlistWin = null;

// 处理格式化的弹幕
function splitDanmu(totalDanmu) {
    for (let dm of totalDanmu) {
        formatMsg(dm);
    }
}

// 更新页面数据
function updateMsg(nn, txt) {
    const content = document.getElementById('messages');
    content.innerHTML += '<tr><td><span class="uname">' + nn + '</span>:' + txt + '</td></tr>';
    // 滚动条始终在最下面
    const pane = document.getElementById('pane');
    pane.scrollTop = pane.scrollHeight;


    if (cfg.desktopDanmu == 'true') {
        console.log('sended');
        desktopDanmuWin.webContents.send('danmu', nn, txt);
    }
}

// 更新观众人数
function updateAudience(content) {
    $('#audience').text(content);
}

// 设置房间号
function setRoomId(roomid) {
    $('#show-roomid').text(roomid);
    const content = document.getElementById('pane');
    content.innerHTML = "<table class='table-striped'><tbody id='messages'></tbody></table>";
    danmu.getChatInfo(roomid, (totalDanmu) => {
        splitDanmu(totalDanmu);
    });
}

// github链接
$(document).ready(function() {
    const playlist = document.getElementById('playlist');
    playlist.addEventListener('click', (event) => {
        if (playlistWin === null) {
            playlistWin = new BrowserWindow({
                width: 200,
                height: 300,
                autoHideMenuBar: true,
                icon: __dirname + '../assets/favicon.ico',
            });
            playlistWin.loadURL(`file://${__dirname}/playlist.html`);

            playlistWin.on('closed', () => {
                playlistWin = null;
            });
        }
    });

    const settings = document.getElementById('settings');
    settings.addEventListener('click', (event) => {
        if (settingsWin === null) {
            settingsWin = new BrowserWindow({
                width: 200,
                height: 150,
                autoHideMenuBar: true,
                icon: __dirname + '../assets/favicon.ico',
            });
            settingsWin.loadURL(`file://${__dirname}/settings.html`);

            settingsWin.on('closed', () => {
                settingsWin = null;
            });
        }
    });

    config.getConfig((data) => {
        cfg = data;
        if (cfg.desktopDanmu == 'true') {   // 桌面弹幕自动打开
            createDesktopDanmu();
        }
    });
});

// 获取roomid
ipcRenderer.on('roomid', (event, arg) => {
    setRoomId(arg);
});

// 更新配置
ipcMain.on('update-config', (event, arg) => {
    cfg = arg;
});

// 更新桌面弹幕设置
ipcMain.on('update-desktopDanmu', (event, arg) => {
    cfg = arg;
    if (cfg.desktopDanmu == 'true') {
        createDesktopDanmu();
    } else if (cfg.desktopDanmu == 'false') {
        desktopDanmuWin.close();
    }
});

function createDesktopDanmu() {
    // 桌面弹幕窗口
    desktopDanmuWin = new BrowserWindow({
        width: 250,
        height: 300,
        autoHideMenuBar: true,
        icon: __dirname + '../assets/favicon.ico',
        frame: false,
        transparent: true,
        resizable: false
    });
    desktopDanmuWin.loadURL(`file://${__dirname}/frameless.html`);
    desktopDanmuWin.setAlwaysOnTop(true);
    desktopDanmuWin.on('closed', () => {
        desktopDanmuWin = null;
        cfg.desktopDanmu = 'false'; // 桌面窗口关闭要更新设置
        if (settingsWin !== null) { // 设置窗口打开时需要更新设置按钮
            settingsWin.webContents.send('close-desktopDanmu');
        }

    });
}

function formatMsg(msg) {
    const DANMU_TYPE = '1';
    const BAMBOO_TYPE = '206';
    const AUDIENCE_TYPE = '207';
    const TU_HAO_TYPE = '306';
    const MANAGER = '60';
    const SP_MANAGER = '120';
    const HOSTER = '90';
    msg = JSON.parse(msg);
    let content = msg.data.content;
    if (msg.type == DANMU_TYPE) {
        const identity = msg.data.from.identity;
        let nickName = msg.data.from.nickName;
        if (cfg.music == 'true') {  // 设置可以开启点歌则处理点歌
            diange([0, nickName, content]);
        }
        if (msg.data.from.sp_identity == SP_MANAGER) {
            nickName = '*超管*' + nickName;
        }
        if (identity == MANAGER) {
            nickName = '*房管*' + nickName;
        } else if (identity == HOSTER) {
            nickName = '*主播*' + nickName;
        }
        updateMsg(nickName, content);
        if (cfg.desktopDanmu == 'false') {
            new Notification(nickName, {
                body: content
            });
        }
    } else if (msg.type == BAMBOO_TYPE) {
        nickName = msg.data.from.nickName;
        diange([1, nickName, content]); // 送竹子送经验
        content = '送给主播[' + content + ']个竹子';
        updateMsg(nickName, content);
        if (cfg.desktopDanmu == 'false') {
            new Notification(nickName, {
                body: content
            });
        }
    } else if (msg.type == TU_HAO_TYPE) {
        nickName = msg.data.from.nickName;
        price = msg.data.content.price;
        diange([2, nickName, content]); // 送猫币送经验
        content = '送给主播[' + price + ']个猫币';
        updateMsg(nickName, content);
        if (cfg.desktopDanmu == 'false') {
            new Notification(nickName, {
                body: content
            });
        }
    } else if (msg.type == AUDIENCE_TYPE) {
        updateAudience(content);
    }
}
