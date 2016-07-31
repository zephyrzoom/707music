const http = require('http');
const net = require('net');
const {shell, ipcRenderer} = require('electron');
const diange = require('./system');

function getChatInfo(roomid) {
    http.get('http://www.panda.tv/ajax_chatinfo?roomid=' + roomid, function(res) {
        res.on('data', function(chunk) {
            const json = JSON.parse(chunk);
            const jsonData = json.data;
            const chatAddr = jsonData.chat_addr_list[0];
            const socketIP = chatAddr.split(':')[0];
            const socketPort = chatAddr.split(':')[1];
            const rid = jsonData.rid;
            const appid = jsonData.appid;
            const authtype = jsonData.authtype;
            const sign = jsonData.sign;
            const ts = jsonData.ts;
            const chatInfo = {
                "socketIP": socketIP,
                "socketPort": socketPort,
                "rid": rid,
                "appid": appid,
                "authtype": authtype,
                "sign": sign,
                "ts": ts
            };
            start(chatInfo);
        });
    });
}

function start(chatInfo) {
    const s = net.connect({
        port: chatInfo.socketPort,
        host: chatInfo.socketIP
    }, function() {
        console.log('connect success');
    });
    const msg = 'u:' + chatInfo.rid +
        '@' + chatInfo.appid +
        '\nk:1\nt:300\nts:' + chatInfo.ts +
        '\nsign:' + chatInfo.sign +
        '\nauthtype:' + chatInfo.authtype;
    sendData(s, msg);
    let completeMsg = [];
    s.on('data', function(chunk) {
        completeMsg.push(chunk);
        chunk = Buffer.concat(completeMsg);
        if (chunk.readInt16BE(0) == 6 && chunk.readInt16BE(2) == 6) {
            console.log('login');
            completeMsg = [];
        } else if (chunk.readInt16BE(0) == 6 && chunk.readInt16BE(2) == 3) {
            const msg = getMsg(chunk);
            if (msg[0].length < msg[1]) {
                console.log('parted');
            } else {
                analyseMsg(msg[0]);
                completeMsg = [];
            }
        } else if (chunk.readInt16BE(0) == 6 && chunk.readInt16BE(2) == 1) {
            console.log('keepalive');
            completeMsg = [];
        } else {
            console.log('error');
            console.log(chunk);
            completeMsg = [];
        }
    });
    setInterval(function() {
        sendKeepalive(s);
    }, 300000);
}

function sendData(s, msg) {
    const data = new Buffer(msg.length + 6);
    data.writeInt16BE(6, 0);
    data.writeInt16BE(2, 2);
    data.writeInt16BE(msg.length, 4);
    data.write(msg, 6);
    s.write(data);
}

function sendKeepalive(s) {
    const data = new Buffer(4);
    data.writeInt16BE(6, 0);
    data.writeInt16BE(0, 2);
    s.write(data);
}

function getMsg(chunk) {
    let msgLen = chunk.readInt16BE(4);
    const msg = chunk.slice(6, 6 + msgLen);
    let offset = 6 + msgLen;
    msgLen = chunk.readInt32BE(offset);
    offset += 4;
    msgInfo = [];
    msgInfo.push(chunk.slice(offset, offset + msgLen));
    msgInfo.push(msgLen);
    return msgInfo;
}

function analyseMsg(totalMsg) {
    while (totalMsg.length > 0) {
        const IGNORE_LEN = 12;
        totalMsg = totalMsg.slice(IGNORE_LEN);
        const msgLen = totalMsg.readInt32BE(0);
        const msg = totalMsg.slice(4, 4 + msgLen);
        formatMsg(msg);
        totalMsg = totalMsg.slice(4 + msgLen);
    }
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
        diange([0, nickName, content]);    // 处理点歌
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
    getChatInfo(roomid);
}

// github链接
$(document).ready(function() {
    const githubLink = document.getElementById('github');
    githubLink.addEventListener('click', function(event) {
        shell.openExternal('http://github.com/zephyrzoom');
    });
});

// 获取roomid
ipcRenderer.on('roomid', (event, arg) => {
    setRoomId(arg);
});
