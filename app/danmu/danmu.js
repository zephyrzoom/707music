const http = require('http');
const net = require('net');


exports.getChatInfo = function getChatInfo(roomid, callback) {
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
            start(chatInfo, (totalDanmu) => {
                if (callback) {
                    callback(totalDanmu);
                }
            });
        });
    });
};

function start(chatInfo, callback) {
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
                const totalDanmu = analyseMsg(msg[0]);
                if (callback) {
                    callback(totalDanmu);
                }
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
    let totalDanmu = [];
    while (totalMsg.length > 0) {
        const IGNORE_LEN = 12;
        totalMsg = totalMsg.slice(IGNORE_LEN);
        const msgLen = totalMsg.readInt32BE(0);
        const msg = totalMsg.slice(4, 4 + msgLen);
        totalDanmu.push(msg);
        // formatMsg(msg);  // for test
        totalMsg = totalMsg.slice(4 + msgLen);
    }
    return totalDanmu;
}
