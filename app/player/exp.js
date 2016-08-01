const fs = require('fs');
const EXP = './exp.json';
let exps;
(function readExps() {
    fs.readFile(EXP, (err, data) => {
        if (err) {
            throw err;
        }
        exps = JSON.parse(data);
    });
}());

exports.getExp = function getExp(id, callback) {
    for (let exp of exps.exps) {
        if (id == exp.id) {
            return exp.exp;
        }
    }
};

exports.updateExp = function updateExp(id, exp) {
    for (let exp of exps.exps) {
        if (id == exp.id) {
            exp.exp = exp;
            return true;
        }
    }
    return false;
};

exports.writeExp = function writeExp() {
    fs.writeFile(EXP, JSON.stringify(exp), (err) => {
        if (err) throw err;
        console.log('saved');
    });
};
