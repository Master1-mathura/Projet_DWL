<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="assets/css/DWL.css">
        <title>Don't WatchList</title>
    </head>
    <body>
        <div id="bg-layer"></div>
        <div id="bg-overlay"></div>
        <header class="dwl-header">
            <a href="MoteurRecherche.php" class="back-link">
                <span class="icon">←</span> Back to Search
            </a>
            <h1><?php echo isset($response) ? $response : 'My Watchlist'; ?></h1>
        </header>

        <div class="app-content">
            <section class="active-info-section">
                <span class="active-badge">Search in progress</span>
                <h1 id="active-title">Loading...</h1>
                <p id="active-synopsis">Select a film from your Watchlist to see its details.</p>
                <div class="action-buttons">
                    <form method="POST" action="DWL.php">
                        <input type="hidden" id="delete-film-id" name="delete_id" value="">
                        <button type="submit" class="btn-primary" style="background: linear-gradient(135deg, #e74c3c, #c0392b);">
                            Remove from Watchlist
                        </button>
                    </form>
                    <form method="POST" action="DWL.php" style="display:flex; gap:10px;">
                        <input type="hidden" id="update-film-id" name="update_id" value="">
                        <select name="nv_etat" id="update-state-select" style="padding: 10px; border-radius: 8px; background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.3);">
                            <option value="En Attente" style="color: black;">En Attente</option>
                            <option value="Survécu" style="color: black;">Survécu</option>
                            <option value="Abandon" style="color: black;">Abandon</option>
                        </select>
                        <button type="submit" class="btn-primary">
                            Update
                        </button>
                    </form>
                </div>
            </section>

            <main class="dwl-container">
                <h2 class="section-title">MY WATCHLIST</h2>
                <div class="carousel-wrapper">
                    <button class="carousel-nav-btn left-btn" onclick="prevMovie()">&#10094;</button>
                    
                    <div class="movie-layout" id="carousel">
                        <?php foreach ($watchlist as $movie) : ?>
                            <article class="movie-card" 
                                    onclick="selectMovie(this)"
                                    data-id="<?= htmlspecialchars($movie['imdb_id']) ?>"
                                    data-bg="<?= htmlspecialchars($movie['background']) ?>"
                                    data-title="<?= htmlspecialchars($movie['film_name']) ?>"
                                    data-state = "<?= htmlspecialchars($movie['etat']) ?>">
                                <div class="card-overlay"></div>
                                <img src="<?= htmlspecialchars($movie['poster']) ?>" alt="Affiche" class="movie-poster">

                                <div class="movie-info">
                                    <h2><?= htmlspecialchars($movie['film_name']) ?></h2>
                                </div>
                            </article>
                        <?php endforeach; ?>
                    </div>
                    <button class="carousel-nav-btn right-btn" onclick="nextMovie()">&#10095;</button>
                </div>
                <div id="carousel-counter">0 / 0</div>
            </main>
        </div>

        <script>
            let currentIndex = 1;
            let totalMovies = 0;
            let movieCards = [];

            function selectMovie(cardElement,index) {
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
                    document.getElementById('active-title').innerText = "Watchlist Vide";
                    document.getElementById('active-synopsis').innerText = "Retournez à la recherche pour ajouter vos pires cauchemars.";
                    document.querySelector('.carousel-wrapper').style.display = 'none';
                    document.getElementById('carousel-counter').style.display = 'none';
                }

                const carousel = document.getElementById('carousel');
                carousel.addEventListener('wheel', (evt) => {
                    evt.preventDefault();
                    carousel.scrollLeft += evt.deltaY;
                });
            };
        </script>
    </body>
</html>