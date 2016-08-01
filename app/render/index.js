const danmu = require('../danmu/danmu');
const { shell, ipcRenderer } = require('electron');
const diange = require('../player/system');

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
    const githubLink = document.getElementById('github');
    githubLink.addEventListener('click', function(event) {
        shell.openExternal('http://github.com/zephyrzoom');
    });

    const playlist = document.getElementById('playlist');
    playlist.addEventListener('click', (event) => {
        const { BrowserWindow } = require('electron').remote;
        let playlistWin = new BrowserWindow({
            width: 200,
            height: 300,
            autoHideMenuBar: true,
            icon: __dirname + '../assets/favicon.ico',
        });
        playlistWin.loadURL(`file://${__dirname}/../render/playlist.html`);

        playlistWin.on('closed', () => {
            playlistWin = null;
        });
    });
});

// 获取roomid
ipcRenderer.on('roomid', (event, arg) => {
    setRoomId(arg);
});

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
        diange([0, nickName, content]); // 处理点歌
        if (msg.data.from.sp_identity == SP_MANAGER) {
            nickName = '*超管*' + nickName;
        }
        if (identity == MANAGER) {
            nickName = '*房管*' + nickName;
        } else if (identity == HOSTER) {
            nickName = '*主播*' + nickName;
        }
        updateMsg(nickName, content);
        new Notification(nickName, {
            body: content
        });
    } else if (msg.type == BAMBOO_TYPE) {
        nickName = msg.data.from.nickName;
        diange([1, nickName, content]); // 送竹子送经验
        content = '送给主播[' + content + ']个竹子';
        updateMsg(nickName, content);
        new Notification(nickName, {
            body: content
        });
    } else if (msg.type == TU_HAO_TYPE) {
        nickName = msg.data.from.nickName;
        price = msg.data.content.price;
        diange([2, nickName, content]); // 送猫币送经验
        content = '送给主播[' + price + ']个猫币';
        updateMsg(nickName, content);
        new Notification(nickName, {
            body: content
        });
    } else if (msg.type == AUDIENCE_TYPE) {
        updateAudience(content);
    }
}
