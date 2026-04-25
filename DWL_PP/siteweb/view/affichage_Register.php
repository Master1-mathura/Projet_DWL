<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>S'inscrire - The Don't Watchlist</title>
        <link rel="stylesheet" href="assets/css/style_login.css">
    </head>
    <body>
        <div class="login-card">

            <img src="assets/images/logo.png" alt="Logo" class="login-logo">

            <h2>Créer un compte</h2>

            <form method="POST">
                <div class="input-group">
                    <label>Nom d'utilisateur :</label>
                    <input type="text" name="username" required>
                </div>

                <div class="input-group">
                    <label>Mot de passe :</label>
                    <input type="password" name="password" required>
                </div>

                <button type="submit" name="register">S'inscrire</button>
            </form>

            <?php if(!empty($error)): ?>
                <p class="msg-error"><?= htmlspecialchars($error) ?></p>
            <?php endif; ?>

            <?php if(!empty($message)): ?>
                <p class="msg-success"><?= htmlspecialchars($message) ?></p>
            <?php endif; ?>

            <div style="margin-top: 20px; text-align: center;">
                <p style="color: var(--text-muted); font-size: 0.9rem;">
                    Déjà un compte ?
                    <a href="Login.php" style="color: var(--primary-light); text-decoration: none; font-weight: bold;">Se connecter</a>
                </p>
            </div>

        </div>
    </body>
</html>