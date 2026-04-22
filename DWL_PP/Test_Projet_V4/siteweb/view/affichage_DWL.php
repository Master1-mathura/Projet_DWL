<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="assets/style.css">
    <title>Don't WatchList</title>
</head>
<body>
    <h1><?php echo $response; ?></h1>

<section>
    <h2>WATCHLIST</h2>
    <ul>
        <li class = "movie_box">
            <?php foreach ($watchlist as $movie) :?>
                <li> 
                    <button class="open-btn" onclick="showDetails('<?= addslashes($movie['id']) ?>')">
                        <?= htmlspecialchars($movie['id']) ?> (<?= $movie['film_name']?>)
                    </button>
                </li>
            <?php endforeach; ?>
        </li>
    </ul>
</section>
</body>
</html>