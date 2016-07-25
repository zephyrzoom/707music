// const {api} = require('NeteaseCloudMusicApi');
// // api.search('理想三旬', data => {
// //   console.log(data);
// // })
// api.song('31445772', data => {
//   console.log(data);
// });
// api.lrc('31445772', data => {
//   console.log(data);
// });


alert('js loaded');

function playMusic() {
  const p = document.getElementById('start');
  p.setAttribute('onclick', () => {
    alert('play');
  });
}

function pauseMusic() {
  alert('pause');
}

document.getElementById('pause').onclick = function () {
  
}

function nextMusic() {
  alert('next');
}

const audio = new Audio('three.mp3');
audio.play();
