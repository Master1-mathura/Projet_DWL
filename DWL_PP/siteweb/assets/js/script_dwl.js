
let currentIndex = 1;
let totalMovies = 0;
let movieCards = [];
let currentFetchId = null;

async function selectMovie(cardElement,index) {
    movieCards.forEach(card => card.classList.remove('active')); 
    cardElement.classList.add('active');
    
    currentIndex = index;
    document.getElementById("carousel-counter").innerText = `${currentIndex} / ${totalMovies}`;
    
    const id = cardElement.getAttribute('data-id');
    const title = cardElement.getAttribute('data-title');
    const state = cardElement.getAttribute('data-state');
    const bgUrl = cardElement.getAttribute('data-bg');
    document.getElementById('delete-film-id').value = id;
    document.getElementById('update-film-id').value = id;
    document.getElementById('update-state-select').value = state;
    document.getElementById('active-title').innerText = title;
    const bgLayer = document.getElementById('bg-layer');
    bgLayer.style.opacity = 0; 
    
    setTimeout(() => {
        bgLayer.style.backgroundImage = `url('${bgUrl}')`;
        bgLayer.style.opacity = 1;
    }, 400); 
    
    cardElement.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });  
    document.getElementById('active-synopsis').innerText = "Loading synopsis...";
    currentFetchId = id;

    try {
        const response = await fetch('DWL.php', {
            method: 'POST',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify({film_ID : id})
        });
        
        const metadata = await response.json();
            if (currentFetchId === id) {
            document.getElementById('active-synopsis').innerText = metadata.synposis || "No synopsis available.";
        }
    } catch(error) {
        console.error("Error while fetching synopsis :", error);
        if (currentFetchId === id) {
            document.getElementById('active-synopsis').innerText = "An error occurred while loading the synopsis.";
        }
    }
}

function prevMovie() {
    if(currentIndex > 1 ){
        selectMovie(movieCards[currentIndex - 2], currentIndex - 1);
    }
    else {
        selectMovie(movieCards[totalMovies -1], totalMovies);
    }
}

function nextMovie(){
    if(currentIndex < totalMovies){
        selectMovie(movieCards[currentIndex],currentIndex + 1);
    }
    else {
        selectMovie(movieCards[0],1)
    }
}

window.onload = () => {
    movieCards = document.querySelectorAll('.movie-card');
    totalMovies = movieCards.length;

    if (totalMovies > 0) {
        movieCards.forEach((card,index) => {
            card.onclick = () => selectMovie(card,index + 1);
        });
        selectMovie(movieCards[0],1);
        
    } else {
        document.getElementById('active-title').innerText = "Empty Watchlist";
        document.getElementById('active-synopsis').innerText = "Go back to search to add your worst nightmares.";
        document.querySelector('.carousel-wrapper').style.display = 'none';
        document.getElementById('carousel-counter').style.display = 'none';
    }

    const carousel = document.getElementById('carousel');
    carousel.addEventListener('wheel', (evt) => {
        evt.preventDefault();
        carousel.scrollLeft += evt.deltaY;
    });
}