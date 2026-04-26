<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Log in - The Don't Watchlist</title>
        <link rel="stylesheet" href="assets/css/login.css">
    </head>
    <body>
        <div class="login-card">
            <img src="assets/images/logo.png" alt="Logo The Don't Watchlist" class="login-logo">
            <h2>Login</h2>

            <form method="POST">
                <div class="input-group">
                    <label>Username :</label>
                    <input type="text" name="username" autocomplete="off" required>
                </div>
                <div class="input-group">
                    <label>Password :</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit" name="connexion">Sign In</button>
            </form>

            <?php if(!empty($error)): ?>
                <p><?= htmlspecialchars($error) ?></p>
            <?php endif; ?>
            <?php if(!empty($message)): ?>
                <p><?= htmlspecialchars($message) ?></p>
                    <script>
                        setTimeout(() => {
                            window.location.href = "MoteurRecherche.php";
                        }, 500);
                    </script>
            <?php endif; ?>
            <div style="margin-top: 20px; text-align: center;">
                <p style="color: var(--text-muted); font-size: 0.9rem;">
                    No account ?
                    <a href="Register.php" style="color: var(--primary-light); text-decoration: none; font-weight: bold;">Create one</a>
                </p>
            </div>
        </div>
    </body>
</html>