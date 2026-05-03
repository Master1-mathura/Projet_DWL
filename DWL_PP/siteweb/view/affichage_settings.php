<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Settings - The Don't Watchlist</title>
        <link rel="stylesheet" href="assets/css/settings.css">
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
            <a href="MyProfile.php" class="settings-link" title="My Profile">
                <img src="assets/images/myprofile.png" alt="Settings Icon" class="settings-icon">
            </a>
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
                <form method="POST" id="deleteForm" class="settings-form" style="margin-top: 15px;">
                    <div class="button-group">
                        <button type="button" id="deleteBtn" name="delete_profile" class="danger-btn">Delete Account</button>
                    </div>
                </form>
            </div>
        </main>
        <div id="deleteOverlay" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); color:white; z-index:9999; flex-direction:column; align-items:center; justify-content:center; text-align:center; font-family: Arial, sans-serif;">            <h2 style="color: #7b58a3;">Account Deletion</h2>
            <p>Your account is being deleted...</p>
            <div id="countdown" style="font-size: 5rem; font-weight: bold; margin: 20px 0;">5</div>
            <p>Redirecting in a few seconds...</p>
        </div>

        <script>
            document.getElementById('deleteBtn').addEventListener('click', function() {
                if (confirm("Are you sure you want to delete your account? This action is irreversible.")) {

                    const overlay = document.getElementById('deleteOverlay');
                    const countdownElement = document.getElementById('countdown');
                    const form = document.getElementById('deleteForm');

                    let timeLeft = 5;

                    // 2. Afficher l'overlay (on force le flex car il est en display:none par défaut)
                    overlay.style.display = 'flex';

                    // 3. Lancer le compte à rebours
                    const timer = setInterval(function() {
                        timeLeft--;
                        countdownElement.textContent = timeLeft;

                        if (timeLeft <= 0) {
                            clearInterval(timer);

                            // 4. Créer un input caché pour que PHP reçoive bien le 'delete_profile'
                            const hiddenInput = document.createElement('input');
                            hiddenInput.type = 'hidden';
                            hiddenInput.name = 'delete_profile';
                            hiddenInput.value = '1';
                            form.appendChild(hiddenInput);

                            // 5. Envoyer le formulaire vers le serveur
                            form.submit();
                        }
                    }, 1000);
                }
            });
        </script>
    </body>
</html>