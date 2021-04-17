let previous = document.querySelector('#pre');
let play = document.querySelector('#play');
let next = document.querySelector('#next');

let title = document.querySelector('#title');
let artist = document.querySelector('#artist');

let recent_volume = document.querySelector('#volume');
let volume_show = document.querySelector('#volume_show');
let track_image = document.querySelector('#track_image');

let slider = document.querySelector('#duration_slider');
let show_duration = document.querySelector('#show_duration');

let auto_play = document.querySelector('#auto');
let present = document.querySelector('#present');
let total = document.querySelector('#total');

let timer;
let autoplay=0;
let index_no=0;
let playing_song = false;

let track=document.createElement('audio');

let all_song=[
    {
        name:"Reflections of Nature",
        path: "https://cdnm.meln.top/mr/Reflections%20of%20Nature%20-%20Jasmine%20Calm.mp3?session_key=94419e6ebb7007426c33fce49e26f740&hash=0202db90f91b475d622002fb7c98ce54",
        img: "https://i.imgur.com/1slUOw9.jpg",
        singer: "Jasmine Calm"
    },
    {   name:"Relaxing Instrumental Jazz",
        path: "https://cdnm.meln.top/mr/Relaxing%20Instrumental%20Jazz%20Ensemble%20-%20Always%20Yours%20Forever%20%28Gentle%20Sleep%20Music%29.mp3?session_key=654a9a96ab5f2e0ff9290ea340a9524b&hash=315f70894b0ddbde6548fb44840fda0b",
        img: "https://i.kfs.io/album/global/33566346,3v1/fit/500x500.jpg",
        singer: "always yours forever"
    },
    {
        name:"Music heals the soul",
        path: "https://cdnm.meln.top/mr/Healing%20Music%20-%2006%20Joy.mp3?session_key=2c10b17a991e6b213fe5e3c7350cc8cb&hash=1fa6fb3458a3df3fbb4aaab26c002da2",
        img: "https://www.hemsworthsbackalright.com/wp-content/uploads/2018/05/stress-relief-music-940x800.jpg",
        singer: "Joy/happiness"
    },
    {
        name:"Keys of Moon",
        path: "https://cdnm.meln.top/mr/Keys%20of%20Moon%20-%20Overcoming%20-%20Epic%20Motivational%20Music.mp3?session_key=b00547060a5fbbe374cf05543f67d640&hash=7ede52c889dae57e69a248d4ef2929d4",
        img: "https://i.ytimg.com/vi/nTLpGRCV22Y/maxresdefault.jpg",
        singer: "Motivation"
    },
    {
        name:"MERLIN magic",
        path: "https://cdnm.meln.top/mr/Merlin%27s%20Magic%20-%20Deep%20in%20My%20Soul.mp3?session_key=f96c7d6a450ab2456e005c9237f35ffd&hash=e525224ed774d08db4cec4525e7c0247",
        img: "https://sites.psu.edu/siowfa16/files/2016/10/music-1wimix9.gif",
        singer: "Soulful Music"
    }
];
function load_track(index_no){
    clearInterval(timer);
    reset_slider();
    track.src = all_song[index_no].path;
    title.innerHTML = all_song[index_no].name;
    track_image.src = all_song[index_no].img;
    artist.innerHTML = all_song[index_no].singer;
    track.load();
    
    total.innerHTML = all_song.length;
    present.innerHTML = index_no+1;
    timer = setInterval(range_slider , 1000);
}
load_track(index_no);

function mute_sound(){
    track.volume = 0;
    volume.value= 0;
    volume_show.innerHTML = 0;
}
function reset_slider(){
    slider.value=0;
}
function justplay(){
    if(playing_song==false){
        playsong();
    }else{
        pausesong();
    }
}
function playsong(){
    track.play();
    playing_song=true;
    play.innerHTML = '<i class="fa fa-pause"></i>';
}
function pausesong(){
    track.pause();
    playing_song=false;
    play.innerHTML = '<i class="fa fa-play"></i>';
}
function next_song(){
    if(index_no < all_song.length-1){
        index_no +=1;
        load_track(index_no);
        playsong();
    }else{
        index_no=0;
        load_track(index_no);
        playsong();
    }
}
function previous_song(){
    if(index_no > 0 ){
        index_no -=1;
        load_track(index_no);
        playsong();
    }else{
        index_no = all_song.length-1 ;
        load_track(index_no);
        playsong();
    }
}
function volume_change(){
    volume_show.innerHTML = recent_volume.value;
    track.volume = recent_volume.value / 100;
}
function change_duration(){
    slider_position = track.duration * (slider.value /100);
    track.currentTime = slider_position;
}
function autoplay_switch(){
    if(autoplay==1){
        autoplay=0;
        auto_play.style.background = "rgba(255,255,255,0.2)";
    }else{
        autoplay=1;
        auto_play.style.background = "rgb(243, 183, 104)";
    }
}

function range_slider(){
    let position=0;
    if(!isNaN(track.duration)){
        position = track.currentTime * (100/track.duration);
        slider.value = position;
    }
    if(track.ended){
        play.innerHTML = '<i class="fa fa-play"></i>';
        if(autoplay==1){
            index_no+=1;
            load_track(index_no);
            playsong();
        }
    }
}

