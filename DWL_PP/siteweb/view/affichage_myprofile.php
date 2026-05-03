<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Profile - The Don't Watchlist</title>
    <link rel="stylesheet" href="assets/css/myprofile.css">
</head>
<body class="theme-<?php echo htmlspecialchars($theme); ?>">
    <header class="main-header">
        <div class="nav">
            <h1>Welcome <span><?php echo htmlspecialchars($username); ?></span></h1>
            <a href="DWL.php" class="watchlist-link" title="Voir ma Watchlist">
                <img src="assets/images/watchlist.png" alt="Watchlist" class="watchlist-icon">
            </a>

            <a href="MoteurRecherche.php" class="nav-link">Search Engine</a>

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
    <main class="profile-container">
        <div class="profile-header">
            <div class="avatar-container">
                <span class="avatar-initial"><?= strtoupper(substr($username, 0, 1)) ?></span>
            </div>
            <div class="profile-info">
                <h2><?php echo htmlspecialchars($username); ?></h2>
            </div>
            <a href="Settings.php" class="settings-link" title="Paramètres">
                <img src="assets/images/settings.png" alt="Settings Icon" class="settings-icon">
            </a>
        </div>
        <div class="stats-grid">
            <div class="stat-card">
                <h3><?php echo htmlspecialchars($nombre_de_films); ?></h3> <p>Movies in Watchlist</p>
            </div>
        </div>
        <section class="settings-content">
            <div class="profile-info">
                <h2>Appearance</h2>
            </div>
            <div class="divider"></div>
            <p>Customize the look and feel of your profile.</p>
            <form method="POST">
                <div class="theme-options">
                    <button class="theme-btn" name="DarkMode">Dark Mode</button>
                    <button class="theme-btn" name="LightMode">Light Mode</button>
                </div>
            </form>
            <form method="POST">
                <input type="hidden" name="cocherBlurPoster" value="1">
                <div class="blur_poster">
                    <label for="blurPoster">Blur Movie Posters:</label>
                    <input type="checkbox" name="blurPoster" onchange="this.form.submit()" <?php if ($isBlurred === "on") echo "checked"; ?>>
                </div>
            </form>
        </section>
        <br>
    </main>
</body>
</html>