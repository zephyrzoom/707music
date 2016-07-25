const neteaseAPI = require('NeteaseCloudMusicApi').api;

let audio = new Audio('http://m2.music.126.net/fzxb9-94aH0yYp8l-s6UvQ==/3250156383168327.mp3');
audio.play();

window.onload = () => {
  document.getElementById('start').onclick = () => {
    audio.play();
  }
  document.getElementById('pause').onclick = () => {
    audio.pause();
  }
  document.getElementById('next').onclick = () => {
    audio.src = 'kenny.mp3';
    audio.play();
  }
  document.getElementById('search').onclick = () => {
    const name = document.getElementById('name').value;
    const result = search(name);
    const render = document.getElementById('result');
    render.innerHTML = result;
  }
}

function search(name) {
  neteaseAPI.search(name, (data) => {
    alert(data);
    return data;
  })
}

function select(songs, num) {
  return JSON.parse(songs).result.songs[num-1].id;
}

function getMusicUrl(id) {
  neteaseAPI.song(id, (data) => {
    return JSON.parse(data).songs[0].mp3Url;
  });
}

function getLrc(id) {
  neteaseAPI.lrc(id, data => {
    return JSON.parse(data).lrc.lyric;
  });
}
