const box = document.getElementById("box-detail");
function openBox(){
    box.style.display = "flex";
}

function closeBox(){
    box.style.display = "none";
}
function closeOnOutsideClick(event){
    if(event.target === box){
        closeBox();
    }
}
async function showDetails(ID) {
    console.log(ID);
    const response = await fetch('MoteurRecherche.php',{
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        body: JSON.stringify({film_ID : ID})
    });
    const metadata = await response.json();
    console.log(metadata);
    document.getElementById("box-title").innerText = metadata.title;
    document.getElementById("box-synposis").innerText = metadata.synposis;

    let valeur = metadata.score;
    let score = Math.round((valeur / 10) * 100);

    let fillBar = document.getElementById("rating-fill");
    let scoreText = document.getElementById("box-score");

    scoreText.innerText = score + "%";

    fillBar.style.width = "0%";
    setTimeout(() => {
        fillBar.style.width = score + "%";
    },50);

    fillBar.className = "rating-fill";

    if(score >= 75){
        fillBar.classList.add("fill-high");
        scoreText.style.color = "#2ecc71";
    }
    else if (score >= 50){
        fillBar.classList.add("fill-medium");
        scoreText.style.color = "#f1c40f";
    }
    else {
        fillBar.classList.add("fill-low");
        scoreText.style.color = "#e74c3c";
    }
    document.getElementById("box-score").innerText = score;
    document.getElementById("box-poster-container").innerHTML = `<img src="${metadata.poster}" class="poster-img" alt="Affiche du film">`;
    document.getElementById("modal-film-id").value = ID;

    openBox();
}
async function ajouterWatchlist(event) {
    event.preventDefault(); //Empeche le formulaire de recharger la page
    const filmID = document.getElementById("modal-film-id").value;

    const formData = new URLSearchParams(); //Les données pour la requête
    formData.append('add_watchlist',filmID);
    try {
        await fetch('', {
            method: 'POST',
            body: formData,
            headers: {'Content-Type' : 'application/x-www-form-urlencoded'}
        });
        alert("Film ajouté à la watchlist");
    } catch(error){
        console.error("Erreur lors de l'ajout :", error);
        alert("Une erreur est survenue.");
    }
}