const fs = require('fs');

const CONFIG_PATH = __dirname + '/../config.json';

let config;

exports.getConfig = function getConfig(callback) {
    fs.readFile(CONFIG_PATH, (err, data) => {
        if (err) throw err;
        config = JSON.parse(data);
        if (callback) {
            callback(config);
        }
    });
};

exports.setConfig = function setConfig(newConfig) {
    config = newConfig;
    fs.writeFile(CONFIG_PATH, JSON.stringify(config), (err) => {
        if (err) throw err;
    });
};
