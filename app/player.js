const neteaseAPI = require('NeteaseCloudMusicApi').api;
const EventEmitter = require('events');
const myEvent = new EventEmitter();

let audio = new Audio('http://m2.music.126.net/fzxb9-94aH0yYp8l-s6UvQ==/3250156383168327.mp3');
audio.play();

window.onload = () => {
  document.getElementById('start').onclick = () => {
    audio.play();
  }
  document.getElementById('pause').onclick = () => {
    audio.pause();
  }

  document.getElementById('search').onclick = () => {
    const name = document.getElementById('name').value;
    search(name);
    myEvent.on('search', (data) => {
      const result = data;
      const render = document.getElementById('result');
      render.innerHTML = result;
    });
  }

  document.getElementById('select').onclick = () => {
    const name = document.getElementById('name').value;
    const render = document.getElementById('result');
    render.innerHTML = select(render.innerHTML, name);
  }

  document.getElementById('next').onclick = () => {
    const render = document.getElementById('result');
    getMusicUrl(render.innerHTML);
    myEvent.on('getMusic', (data) => {
      audio.src = data;
      audio.play();
    });
  }
}

function search(name) {
  neteaseAPI.search(name, (data) => {
    myEvent.emit('search', data);
  });
}



function select(songs, num) {
  return JSON.parse(songs).result.songs[num-1].id;
}

function getMusicUrl(id) {
  neteaseAPI.song(id, (data) => {
    myEvent.emit('getMusic', JSON.parse(data).songs[0].mp3Url);
  });
}

function getLrc(id) {
  neteaseAPI.lrc(id, data => {
    return JSON.parse(data).lrc.lyric;
  });
}
