const neteaseAPI = require('NeteaseCloudMusicApi').api;
const http = require('http');
const logger = require('../util/log');
const { ipcMain } = require('electron').remote;

let audio = new Audio();
let searchList;
let mp3Url;
let id;
let playlist = [];
let musicName;

exports.search = function search(name, callback) {
    neteaseAPI.search(name, (data) => {
        searchList = data;
        if (callback) {
            callback(data);
        }
    });
};

exports.select = function select(num) {
    id = JSON.parse(searchList)[num - 1].id;
    console.log(id);
    if (id) {
        getMusicUrl();
    }
};

exports.cut = function cut() {
    logger.log('切歌成功');
    playlist.shift();
    logger.updateList(playlist);
    if (playlist.length) {
        play();
    } else {
        audio.pause();
    }
};

function getMusicUrl() {
    neteaseAPI.song(id, (data) => {
        const song = JSON.parse(data).songs[0];
        musicName = song.name;
        mp3Url = song.mp3Url;
        console.log('get music url', mp3Url);
        http.get(mp3Url, (res) => {
            console.log(res.statusCode);
            if (res.statusCode !== 404) {
                logger.log('点歌成功');
                if (!playlist.length) {
                    playlist.push([musicName, mp3Url]);
                    play();
                } else {
                    playlist.push([musicName, mp3Url]);
                }
                logger.updateList(playlist);
            }
        });
    });
}

function getLrc(id) {
    neteaseAPI.lrc(id, data => {
        return JSON.parse(data).lrc.lyric;
    });
}

function play() {
    audio.src = playlist[0][1];
    audio.play();
}

audio.addEventListener('ended', () => {
    playlist.shift();
    logger.updateList(playlist);
    if (playlist.length) {
        play();
    }
});

ipcMain.on('getList', (event, arg) => {
    event.sender.send('playlist', playlist);
});
