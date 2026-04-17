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
    .add-btn {
        background: transparent;
        border: 1px solid #cbd5e1;
        color: #475569;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        margin-left: 20px; 
    }
    form {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 30px;
            background: #ffffff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        label {
            font-weight: 600;
            color: #555;
        }

        .search-group {
            display: flex;
            gap: 10px;
        }

        input[type="text"] {
            flex-grow: 1;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus {
            border-color: #3b82f6;
            outline: none;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        button[type="submit"] {
            background-color: #2c3e50;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        button[type="submit"]:hover {
            background-color: #1a252f;
        }
</style>
</head>
<body>
    <h1 style="text-transform:uppercase">The Don't Watchlist Search Engine</h1>
    <form method = "post">
        <label for="name">What are you afraid of ?</label>
        <div class="search-group">
            <input type="text" name = "query" autocomplete="off" required>
            <button type="submit">Search</button>
        </div>
    </form>
    <a href="DWL.php">
        <img src="assets/images/watchlist.png" width=100>
    </a>


    <?php if (!empty($searchResults)) : ?>
            <?php foreach ($searchResults as $film) : ?>
                <div class="result-row">                    
                    <div class="color-bar" style="background-color: <?= $film['color'] ?>;">
                        <?= htmlspecialchars($film['film_name']) ?> 
                        <span style="font-size: 0.8em; margin-left: 10px;">
                            (Score: <?= round($film['score'], 2) ?>)
                        </span>
                    </div>

                    <form method="POST" action="add_movie.php" style="margin: 0; box-shadow: none; padding: 0; background: transparent;">
                        <input type="hidden" name="film_name" value="<?= htmlspecialchars($film['film_name']) ?>">
                        <button type="submit" class="add-btn">Add</button>
                    </form>
                </div>
            <?php endforeach; ?>            
        <?php elseif (isset($_POST["query"])) : ?>
            <p>Aucun film trouvé pour cette recherche.</p>
        <?php endif; ?>
</body>
</html>