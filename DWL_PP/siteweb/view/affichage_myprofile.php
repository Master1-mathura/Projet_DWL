<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Profile - The Don't Watchlist</title>
        <link rel="stylesheet" href="assets/css/myprofile.css">
    </head>
    <body>
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
        <?php if (isset($error) || isset($message)): ?>
            <div class="popup-notification <?php echo isset($error) ? 'popup-error' : 'popup-success'; ?>" id="popupNotification">
                <div class="popup-content">
                    <?php echo isset($error) ? htmlspecialchars($error) : htmlspecialchars($message); ?>
                </div>
                <button class="popup-close" onclick="document.getElementById('popupNotification').style.display='none'">&times;</button>
            </div>
        <?php endif; ?>
        <main class="profile-container">
            <div class="profile-header">
                <div class="avatar-container">
                    <span class="avatar-initial"><?= strtoupper(substr($username, 0, 1)) ?></span>
                </div>
                <div class="profile-info">
                    <h2><?php echo htmlspecialchars($username); ?></h2>
                </div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <h3><?php echo htmlspecialchars($nombre_de_films); ?></h3> <p>Movies in Watchlist</p>
                </div>
            </div>

            <div class="divider"></div>
            <div class="settings-section">
                <h3>Account Settings</h3>

                <form method="POST" class="settings-form">
                    <div class="input-group">
                        <label for="new_username">New Username</label>
                        <input type="name" id="new_username" name="new_username" placeholder = "Your new username ?"  autocomplete = "off">
                    </div>

                    <div class="input-group">
                        <label for="old_password">Old Password</label>
                        <input type="password" id="old_password" name="old_password" placeholder="Leave blank to keep current">
                    </div>
                    <div class="input-group">
                        <label for="new_password">New Password</label>
                        <input type="password" id="new_password" name="new_password" placeholder="Leave blank to keep current">
                    </div>

                    <div class="button-group">
                        <button type="submit" name="update_profile" class="save-btn">Save Changes</button>
                    </div>
                </form>
            </div>
        </main>
    </body>
</html>