const fs = require('fs');
const util = require('util');

const log_file = fs.createWriteStream(__dirname + '/../log/log.txt', {flags : 'w'});
const playlist_file = __dirname + '/../log/playlist.txt';

exports.log = function log(message) {
    message = new Date().toLocaleString() + " " + message;
    log_file.write(util.format(message) + '\n');
};

exports.updateList = function updateList(playlist) {    // playlist是mp3url的数组
    let list = '播放列表\n';
    for (let i in playlist) {
        list = list + (Number(i) + 1) + '. ' + playlist[i][0] + '\n';
    }
    fs.writeFile(playlist_file, list, (err) => {
        if (err) throw err;
    });
};
