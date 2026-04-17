<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/style.css">
    <title>SEARCH BAR</title>
    <style>
    .result-row { display: flex; align-items: center; margin-bottom: 10px; gap: 10px; }
    .color-bar { flex-grow: 1; padding: 10px; color: white; border-radius: 5px; min-width: 200px; }
    .add-btn { padding: 5px 10px; cursor: pointer; }
</style>
</head>
<body>
    <h1 style="text-transform:uppercase">The Don't Watchlist Search Engine</h1>
    <form method = "post">
        <label for="name">What are you afraid of ?</label>
        <input type="text" name = "query" autocomplete="off" required>
        <button type="submit">Search</button>
    </form>
    <a href="DWL.php">
        <img src="assets/images/watchlist.png" width=100>
    </a>


    <?php if (!empty($searchResults)) : ?>
            <?php foreach ($searchResults as $film) : ?>
                <div class="result-row">
                    <span style="font-size: 20px; font-weight: bold;">*</span>
                    
                    <div class="color-bar" style="background-color: <?= $film['color'] ?>;">
                        <?= htmlspecialchars($film['film_name']) ?> 
                        <span style="font-size: 0.8em; margin-left: 10px;">
                            (Score: <?= round($film['score'], 2) ?>)
                        </span>
                    </div>

                    <button class="add-btn">Add</button>
                </div>
            <?php endforeach; ?>
            
            <button style="margin-top: 20px; padding: 5px 20px;">OK</button>
            
        <?php elseif (isset($_POST["query"])) : ?>
            <p>Aucun film trouvé pour cette recherche.</p>
        <?php endif; ?>
</body>
</html>