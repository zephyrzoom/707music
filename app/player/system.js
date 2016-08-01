const danmuParse = require('./parse');
const player = require('./player');

function getDanmu(danmu) {
    const diange = danmuParse(danmu[2]);
    if (diange && diange[0] === 'diange') {
        player.search(diange[1], () => {
            player.select(1);
        });
    }

    if (diange && diange[0] === 'choose') {
        // player.select(diange[1]);
    }

    if (diange && diange[0] === 'cut') {
        player.cut();
    }
}
module.exports = getDanmu;
