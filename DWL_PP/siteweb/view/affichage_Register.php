<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Register - The Don't Watchlist</title>
        <link rel="stylesheet" href="assets/css/register.css">
    </head>
    <body>
        <div class="login-card">

            <img src="assets/images/logo.png" alt="Logo" class="login-logo">

            <h2>Create account</h2>

            <form method="POST">
                <div class="input-group">
                    <label>User name :</label>
                    <input type="text" name="username" autocomplete="off" required>
                </div>

                <div class="input-group">
                    <label>Password :</label>
                    <input type="password" name="password" autocomplete="off" required>
                </div>

                <button type="submit" name="register">Register</button>
            </form>

            <?php if(!empty($error)): ?>
                <p class="msg-error"><?= htmlspecialchars($error) ?></p>
            <?php endif; ?>

            <?php if(!empty($message)): ?>
                <p class="msg-success"><?= htmlspecialchars($message) ?></p>
            <?php endif; ?>

            <div style="margin-top: 20px; text-align: center;">
                <p style="color: var(--text-muted); font-size: 0.9rem;">
                    You already have an account ?
                    <a href="Login.php" style="color: var(--primary-light); text-decoration: none; font-weight: bold;">Log in</a>
                </p>
            </div>

        </div>
    </body>
</html>