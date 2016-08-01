const regDiange = /^\s*点歌\s*(.*\S)\s*/;
const regChoose = /^\s*选歌\s*(\d+)\s*$/;
const regCut = /^\s*切歌\s*(\d*)\s*$/;
const regLevel = /^\s*等级\s*$/;
const regExp = /^\s*经验\s*$/;
const regJump = /^\s*插队\s*$/;
const regSendExp = /^\s*赠送\s*(\S+)\s+(\d+)\s*$/;

function parse(danmu) {
    let matched;
    matched = regDiange.exec(danmu);
    if (matched) {
        return ['diange', matched[1]];
    }
    matched = regChoose.exec(danmu);
    if (matched) {
        return ['choose', matched[1]];
    }
    matched = regCut.exec(danmu);
    if (matched) {
        if (matched[1]) {
            return ['cut', matched[1]];
        } else {    // 没有序号切第一首
            return ['cut', '1'];
        }
    }
    matched = regLevel.exec(danmu);
    if (matched) {
        return ['level'];
    }
    matched = regExp.exec(danmu);
    if (matched) {
        return ['exp'];
    }
    matched = regJump.exec(danmu);
    if (matched) {
        return ['jump'];
    }
    matched = regSendExp.exec(danmu);
    if (matched) {
        return ['send', matched[1], matched[2]];
    }
}
module.exports = parse;
