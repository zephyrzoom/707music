const {api} = require('NeteaseCloudMusicApi');
// api.search('理想三旬', (data) => {
//   console.log(JSON.parse(data).result.songs[0].id);
// }, 10);
api.song('31445772', (data) => {
    console.log(data);
  console.log(JSON.parse(data).songs[0].mp3Url);
});
// api.lrc('31445772', data => {
//   console.log(JSON.parse(data).lrc.lyric);
// });
