const neteaseAPI = require('NeteaseCloudMusicApi').api;
const http = require('http');

let audio = new Audio();
let searchList;
let mp3Url;
let id;
let playlist = [];

exports.search = function search(name, callback) {
    neteaseAPI.search(name, (data) => {
        searchList = data;
        if (callback) {
            callback(data);
        }
    });
};

exports.select = function select(num) {
    id = JSON.parse(searchList).result.songs[num - 1].id;
    console.log(id);
    if (id) {
        getMusicUrl();
    }
};

exports.cut = function cut() {
    playlist.shift();
    if (playlist.length) {
        play();
    } else {
        audio.pause();
    }
};

function getMusicUrl() {
    neteaseAPI.song(id, (data) => {
        console.log(data);
        mp3Url = JSON.parse(data).songs[0].mp3Url;
        http.get(mp3Url, (res) => {
            console.log(res.statusCode);
            if (res.statusCode !== 404) {
                if (!playlist.length) {
                    playlist.push(mp3Url);
                    play();
                } else {
                    playlist.push(mp3Url);
                }
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
    audio.src = playlist[0];
    audio.play();
}

audio.addEventListener('ended', () => {
    playlist.shift();
    if (playlist.length) {
        play();
    }
});
