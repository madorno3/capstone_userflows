// let search_button = document.getElementById("search-btn");
// let artistInput = document.getElementById("artist");
// let songInput = document.getElementById("title");
let search_btn = document.getElementById("search_btn");
let songInfoDiv = document.getElementById("song-details-div");
let lyricsDiv = document.getElementById("lyrics-div");
let fields = document.getElementById("fields");

search_btn.addEventListener("click", function(e){
    console.log("clicked");
    e.preventDefault();
    songInfoDiv.style.visibility = "visible";
    lyricsDiv.style.visibility = "visible";
})



// async function findLyrics(){
//     let artist = artistInput.value;
//     let song = songInput.value;
//     console.log(artist + song);
//     let res = await axios.get(`https://api.lyrics.ovh/v1/${artist}/${song}`);
//     console.log(res);


    
//     let songh2 = document.createElement("h2");
//     songh2.innerHTML = "";
    
//     songInfoDiv.appendChild(songh2); 
//     songh2.innerHTML =`${song}`;
//     let artisth3 = document.createElement("h3");
//     artisth3.innerHTML = "";
//     songInfoDiv.appendChild(artisth3);
//     artisth3.innerHTML = `By: ${artist}`;
    
    

//     lyricsDiv.innerHTML = "";
//     songInfoDiv.appendChild(lyricsDiv);


//     lyricsDiv.innerHTML = res.data.lyrics;
//     let button = document.createElement("button");
//     button.innerText = "Share Lyrics";
//     songInfoDiv.appendChild(button);
//     button.addEventListener("click", function(e) {
//         e.preventDefault();
//         console.log("clicked");
//     })
    

// }

// search_button.addEventListener("click", function(e) {
//     e.preventDefault();
//     findLyrics();
//     artistInput.value = "";
//     songInput.value = "";

//     console.log("clicked");
// })


// async function findLyrics() {
//     let artist = artistInput.value;
//     let song = songInput.value;
//     console.log(artist + song);
    
//     try {
//         let res = await axios.get(`https://api.lyrics.ovh/v1/${artist}/${song}`);
        
//         console.log(res.data);  // Log the raw response data
        
//         let songInfoDiv = document.createElement("div");
//         songInfoDiv.classList.add("lyrics-div");
//         let songH2 = document.createElement("h2");
//         songH2.textContent = song;
//         let artistH3 = document.createElement("h3");
//         artistH3.textContent = `By: ${artist}`;
//         document.body.appendChild(songInfoDiv);
//         songInfoDiv.appendChild(songH2); 
//         songInfoDiv.appendChild(artistH3);
        
//         let lyricsDiv = document.createElement("div");
//         let lyricsText = res.data.lyrics;
        
//         // Create a scrollable container for long lyrics
//         let lyricsContainer = document.createElement("div");
//         lyricsContainer.style.maxHeight = "500px";
//         lyricsContainer.style.overflowY = "auto";
//         lyricsContainer.innerHTML = lyricsText;
        
//         songInfoDiv.appendChild(lyricsContainer);
        
//     } catch (error) {
//         console.error("Error fetching lyrics:", error.message);
//         let errorMessageDiv = document.createElement("div");
//         errorMessageDiv.textContent = `Failed to load lyrics. Error: ${error.message}`;
//         songInfoDiv.appendChild(errorMessageDiv);
//     }
// }

// search_button.addEventListener("click", function(e) {
//     e.preventDefault();
//     findLyrics();
//     artistInput.value = "";
//     songInput.value = "";
//     console.log("clicked");
// })


// async function findLyrics(){
//     let artist = artistInput.value;
//     let song = songInput.value;
//     console.log(artist + song);
//     let res = await axios.get(`https://api.lyrics.ovh/v1/${artist}/${song}`);
//     console.log(res);
//     let songInfoDiv = document.createElement("div");
//     songInfoDiv.classList.add("lyrics-div");
//     let songH2 = document.createElement("h2");
//     songH2.innerHTML = song;
//     let artistH3 = document.createElement("h3");
//     artistH3.textContent = `"By:" ${artist}`;
//     document.body.appendChild(songInfoDiv);
//     songInfoDiv.appendChild(songH2); 
//     songInfoDiv.appendChild(artistH3);
//     let lyricsDiv = document.createElement("div");
//     lyricsDiv.innerHTML = res.data.lyrics;
//     songInfoDiv.appendChild(lyricsDiv);

// }

