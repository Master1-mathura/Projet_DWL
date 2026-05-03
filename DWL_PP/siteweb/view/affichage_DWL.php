<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="assets/css/DWL.css">
        <title>Don't WatchList</title>
    </head>
    <body class="theme-<?php echo htmlspecialchars($theme); ?>">
        <div id="bg-layer" style="<?= ($_SESSION['isBlurred'] === 'on') ? 'filter: blur(10px);' : '' ?>"></div>
        <div id="bg-overlay"></div>
        <header class="main-header">
            <div class="nav">
                <h1>Welcome <span><?php echo htmlspecialchars($username); ?></span></h1>
                <a href="MoteurRecherche.php" class="watchlist-link" title="Voir ma Watchlist">
                    <p>Search Engine</p>
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
                            <option value="En Attente" style="color: black;">Waiting</option>
                            <option value="Survécu" style="color: black;">Survived</option>
                            <option value="Abandon" style="color: black;">Dropped</option>
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
                                <img src="<?= htmlspecialchars($movie['poster'])?>" alt="Affiche" class="movie-poster" style="<?= ($_SESSION['isBlurred'] === 'on') ? 'filter: blur(1px);' : '' ?>">

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
        <script src="assets/js/script_dwl.js"></script>
    </body>
</html>