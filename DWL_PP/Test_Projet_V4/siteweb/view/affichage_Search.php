<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/styl.css">
    <title>SEARCH BAR</title>
</head>
<body>
    <style>
        .result-row { display: flex; align-items: center; margin-bottom: 10px; gap: 10px; }
        .color-bar { flex-grow: 1; padding: 10px; color: white; border-radius: 5px; min-width: 200px; }
        .add-btn {
            background: transparent;
            border: 1px solid #cbd5e1;
            color: #475569;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            margin-left: 20px;
        }
        form {
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-bottom: 30px;
                background: #ffffff;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            }

            label {
                font-weight: 600;
                color: #555;
            }

            .search-group {
                display: flex;
                gap: 10px;
            }

            input[type="text"] {
                flex-grow: 1;
                padding: 12px 15px;
                border: 1px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.2s;
            }

            input[type="text"]:focus {
                border-color: #3b82f6;
                outline: none;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }

            button[type="submit"] {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: background-color 0.2s;
            }

            button[type="submit"]:hover {
                background-color: #1a252f;
            }
    .popup-overlay {
        display: none; /* caché par défaut */
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
    }

    /* BOÎTE DU POPUP */
    .popup-box {
        background: white;
        width: 300px;
        margin: 100px auto;
        padding: 15px;
        border: 1px solid #000;
    }

    /* BOUTON FERMER */
    .close-btn {
        float: right;
        cursor: pointer;
        border: none;
        background: none;
        font-size: 18px;
    }
    </style>
    <header class="main-header">
        <h1>The Don't Watchlist Search Engine</h1>
        <a href="DWL.php" class="watchlist-link" title="Voir ma Watchlist">
        </a>
    </header>
    <main class="container">
        <form method = "post" class="search-form">
            <label for="query">What are you afraid of ?</label>
            <div class="search-group">
                <input type="text" id="query" name="query" autocomplete="off" required>
                <button type="submit">Proteger</button>
            </div>
        </form>

        <div class="results-container">
            <?php if (!empty($searchResults)) : ?>
                <?php foreach ($searchResults as $film) : ?>
                    <div class="result-row">
                        <button  class="open-btn" onclick="showDetails('<?= addslashes($film['id']) ?>')">
                            <div class="color-bar" style="background-color: <?= $film['color'] ?>;">
                                <span class="film-id">ID : (<?= htmlspecialchars($film['id'])?>)</span>
                                <span class="film-title"><?= htmlspecialchars($film['film_name']) ?></span>
                                <span class="film-score">(Score: <?= round($film['score'], 2) ?>)</span>
                            </div>
                        </button>
                    </div>
                <?php endforeach; ?>
            <?php elseif (isset($_POST["query"])) : ?>
                <p class="no-results">Aucun film trouvé pour cette recherche.</p>
            <?php endif; ?>
        </div>
    </main>
    <div id="box-detail" class="box-overlay" onclick="closeOnOutsideClick(event)">
        <div class="modal-content premium-modal">
            <button class="close-btn" onclick="closeBox()">&times;</button>

            <div class="modal-layout">
                <div id="box-poster-container" class="modal-poster-side"></div>

                <div class="modal-info-side">
                    <span class="modal-badge">MOVIE DETAILS</span>
                    <h2 id="box-title"></h2>

                    <div class="rating-bar-container">
                        <div class="rating-track">
                            <div class="rating-fill" id="rating-fill"></div>
                            <span class="score-text" id="box-score"></span>
                        </div>
                    </div>
                    <p id="box-synposis"></p>
                    <form onsubmit="ajouterWatchlist(event)" class="modal-form">
                        <input type="hidden" id="modal-film-id" name="add_watchlist" value="">
                        <button type="submit" class="premium-add-btn">
                            <span class="icon">+</span> Add to Watchlist
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <script>
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
    </script>
</body>
</html>