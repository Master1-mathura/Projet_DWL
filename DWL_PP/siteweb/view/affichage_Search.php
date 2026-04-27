<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/css/search.css">
    <title>SEARCH BAR</title>
</head>
<body>
    <header class="main-header">
        <div class="nav">
            <h1>Welcome <span><?php echo htmlspecialchars($username); ?></span></h1>
            <a href="DWL.php" class="watchlist-link" title="Voir ma Watchlist">
                <img src="assets/images/watchlist.png" alt="Watchlist" class="watchlist-icon">
            </a>
            <a href="MyProfile.php" class="watchlist-link" title="Mon Profil">
                <p>My Profile</p>
            </a>
            <form method="POST" action="MoteurRecherche.php">
                <?php
                    if ($username != "Unknown") {
                        $btnClass = "btn-logout";
                        $btnText = "← Log Out";
                    } else {
                        $btnClass = "btn-login";
                        $btnText = "→ Log In";
                    }
                ?>
                <button type="submit" name="connexion-deconnexion" class="<?php echo $btnClass; ?>">
                    <?php echo $btnText; ?>
                </button>
            </form>
        </div>
        <img src="assets/images/logo.png" alt="Logo The Don't Watchlist" class="main-logo">
        <h1>The Don't Watchlist Search Engine</h1>
    </header>
    <main class="container">
        <form method = "get" class="search-form">
            <label for="query">What are you afraid of ?</label>
            <div class="search-group">
               <input type="text" id="query" name="requete" autocomplete="off" required>
                <button type="submit">Search</button>
            </div>
        </form>

        <div class="results-container">
            <?php if (isset($api_error)) : ?>
                <div style="text-align: center; margin-top: 50px; padding: 40px 20px; background: rgba(26, 19, 37, 0.4); border: 1px solid rgba(187, 164, 214, 0.1); border-radius: 16px; backdrop-filter: blur(5px);">
                    <h3 style="color: var(--primary-light); font-weight: 500; font-size: 1.2rem; letter-spacing: 2px; margin-bottom: 12px; text-transform: uppercase;">Initialization in progress.</h3>
                    <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;">The AI model is finalizing its loading.<br>Please refresh the page in a moment.</p>
                </div>
                
            <?php elseif (!empty($searchResults)) : ?>
                <?php foreach ($searchResults as $film) : ?>
                    <div class="result-row">
                        <button class="open-btn" onclick="showDetails('<?= addslashes($film['id']) ?>')">
                            <div class="color-bar" style="background-color: <?= $film['color'] ?>;">
                                <span class="film-id">ID : (<?= htmlspecialchars($film['id'])?>)</span>
                                <span class="film-title"><?= htmlspecialchars($film['film_name']) ?></span>
                                <span class="film-score">(Score: <?= round($film['score'], 2) ?>)</span>
                            </div>
                        </button>
                    </div>
                <?php endforeach; ?>
                
            <?php elseif (isset($_GET["requete"])) : ?>
                <p class="no-results" style="text-align: center; color: var(--text-muted); font-style: italic; margin-top: 40px;">No movies found.</p>
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
        const currentUsername = "<?= addslashes($username) ?>";
    </script>
    <script src="assets/js/script_moteur.js"> </script>
</body>
</html>