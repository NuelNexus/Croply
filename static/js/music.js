const tracks = [
{
    title:"Alex Skrindo - Me & You",
    album:"Me & You",
    image:"https://singhimalaya.github.io/Codepen/assets/img/album-arts/1.jpg",
    src:"https://singhimalaya.github.io/Codepen/assets/music/1.mp3"
},
{
    title:"Skylike - Dawn",
    album:"Dawn",
    image:"https://singhimalaya.github.io/Codepen/assets/img/album-arts/2.jpg",
    src:"https://singhimalaya.github.io/Codepen/assets/music/2.mp3"
},
{
    title:"Kaaze - Electro Boy",
    album:"Electro Boy",
    image:"https://singhimalaya.github.io/Codepen/assets/music/3.mp3",
    src:"https://singhimalaya.github.io/Codepen/assets/music/3.mp3"
}
];

let currentTrack = 0;
let audio = new Audio();

const albumName = document.getElementById("album-name");
const trackName = document.getElementById("track-name");
const albumImage = document.getElementById("album-image");

const playBtn = document.getElementById("play-pause-button");
const nextBtn = document.getElementById("play-next");
const prevBtn = document.getElementById("play-previous");

const seekBar = document.getElementById("seek-bar");

function loadTrack(index){
    audio.src = tracks[index].src;

    albumName.textContent = tracks[index].album;
    trackName.textContent = tracks[index].title;
    albumImage.src = tracks[index].image;
}

function togglePlay(){

    if(audio.paused){
        audio.play();
        playBtn.innerHTML =
            '<i class="fas fa-pause"></i>';
    }else{
        audio.pause();
        playBtn.innerHTML =
            '<i class="fas fa-play"></i>';
    }
}

function nextTrack(){
    currentTrack++;

    if(currentTrack >= tracks.length){
        currentTrack = 0;
    }

    loadTrack(currentTrack);
    audio.play();

    playBtn.innerHTML =
        '<i class="fas fa-pause"></i>';
}

function prevTrack(){
    currentTrack--;

    if(currentTrack < 0){
        currentTrack = tracks.length - 1;
    }

    loadTrack(currentTrack);
    audio.play();

    playBtn.innerHTML =
        '<i class="fas fa-pause"></i>';
}

audio.addEventListener("timeupdate", () => {

    const progress =
        (audio.currentTime / audio.duration) * 100;

    seekBar.style.width =
        progress + "%";
});

playBtn.addEventListener("click", togglePlay);
nextBtn.addEventListener("click", nextTrack);
prevBtn.addEventListener("click", prevTrack);

loadTrack(0);