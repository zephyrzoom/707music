const {api} = require('NeteaseCloudMusicApi');
// api.search('alice', (data) => {
//   console.log(JSON.parse(data).result.songs[0].id);
// }, 10)
api.song('16432077', (data) => {
  console.log(JSON.parse(data).songs[0].mp3Url);
});
api.lrc('31445772', data => {
  console.log(JSON.parse(data).lrc.lyric);
});
