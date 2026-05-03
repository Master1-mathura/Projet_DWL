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
        <section class="badges-section">
            <div class="badges-info">
                <h2>Badges</h2>
                <div class="divider"></div>
                <p>Earn badges by engaging with the platform and showcasing your movie preferences.</p>

                <div class="badges-container">
                    <?php foreach($tous_les_badges as $badges):
                        $nomBadge = $badges['name'];
                        $estDebloque = in_array($nomBadge, $badge_debloques);

                        $dataSaved = $estDebloque ? "true" : "false";
                        $isLockedClass = $estDebloque ? "badge-icon" : "badge-icon locked";
                        $seuil = $badges['valeur'];
                        $typeCondition = $badges['type'];
                        ?>
                        <img src="assets/images/badges/<?php echo htmlspecialchars($nomBadge); ?>.png"
                             alt="<?php echo htmlspecialchars($nomBadge); ?>"
                             class="<?php echo $isLockedClass; ?>"
                             data-value="<?php echo htmlspecialchars($nomBadge); ?>"
                             title = "<?php echo htmlspecialchars($badges['description']); ?>"
                             data-threshold="<?php echo $seuil; ?>"
                             data-type="<?php echo $typeCondition; ?>"
                             data-saved="<?php echo $dataSaved; ?>">
                    <?php endforeach; ?>
                </div>
            </div>
        </section>
        <div id="badgeModal" class="modal">
            <div class="modal-content">
                <span class="close-modal">&times;</span>
                <div class="modal-body">
                    <img id="modalBadgeImg" src="" alt="Badge Icon">
                    <h2 id="modalBadgeName"></h2>
                    <div class="divider"></div>
                    <p id="modalBadgeDesc"></p>

                    <div id="badgeStatus" class="status-btn"></div>
                </div>
            </div>
        </div>
    </main>

    <script>
        const nbDeFilm = <?php echo isset($nombre_de_films) ? $nombre_de_films : 0; ?>;
        const nbSurvecu = <?php echo isset($survecu) ? $survecu : 0; ?>;
        const nbAbandonne = <?php echo isset($abandonne) ? $abandonne : 0; ?>;

        const badges = document.querySelectorAll('.badge-icon');
        const modal = document.getElementById("badgeModal");
        const closeModal = document.querySelector(".close-modal");

        closeModal.onclick = () => modal.style.display = "none";
        window.onclick = (event) => { if (event.target == modal) modal.style.display = "none"; }

        badges.forEach(badge => {

            const badgeValue = parseInt(badge.getAttribute('data-threshold'));
            const badgeType = badge.getAttribute('data-type');

            let valeurAComparer = 0;
            if (badgeType === "watchlist") {
                valeurAComparer = nbDeFilm;
            } else if (badgeType === "survie") {
                valeurAComparer = nbSurvecu;
            } else if (badgeType === "abandon") {
                valeurAComparer = nbAbandonne;
            }

            if (valeurAComparer >= badgeValue) {
                badge.classList.remove('locked');

                if (badge.getAttribute('data-saved') === "false") {
                    fetch('MyProfile.php', {
                        method: 'POST',
                        body: JSON.stringify({ badgeName: badge.getAttribute('data-value') }),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        badge.setAttribute('data-saved', 'true');
                        console.log("Badge " + badge.getAttribute('data-value') + " sauvegardé en base de données !");
                    })
                    .catch(error => console.error('Error:', error));
                }
            }

            badge.addEventListener('click', () => {
                const isUnlocked = !badge.classList.contains('locked');

                const name = badge.getAttribute('data-value');
                const desc = badge.getAttribute('title');
                const imgSrc = badge.getAttribute('src');

                document.getElementById("modalBadgeImg").src = imgSrc;
                document.getElementById("modalBadgeName").innerText = name;
                document.getElementById("modalBadgeDesc").innerText = desc;

                const statusDiv = document.getElementById("badgeStatus");

                if (isUnlocked) {
                    statusDiv.innerText = "Unlocked";
                    statusDiv.className = "status-btn status-unlocked";
                    document.getElementById("modalBadgeImg").style.filter = "none";
                } else {
                    statusDiv.innerText = "Locked";
                    statusDiv.className = "status-btn status-locked";
                    document.getElementById("modalBadgeImg").style.filter = "grayscale(100%) opacity(40%)";
                }

                modal.style.display = "block";
            });
        });
    </script>
</body>
</html>