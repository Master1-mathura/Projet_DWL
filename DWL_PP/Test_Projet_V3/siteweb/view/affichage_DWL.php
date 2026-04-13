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
        <?php $etiquette = "RED"; // ou "BLUE", "gold", "#ff00ff"... ?>
        <li class = "movie_box" style="background-color: color-mix(in srgb, <?php echo strtolower($etiquette); ?> 40%, transparent);">
            <img src="https://m.media-amazon.com/images/M/MV5BNThiZjA3MjItZGY5Ni00ZmJhLWEwN2EtOTBlYTA4Y2E0M2ZmXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg" 
                    alt="Poster de Spider-Man : Across the Spider-Verse" 
                    width=150>
            
            <div>
                <h3>Spider-Man : Across the Spider-Verse</h3>
                <p>
                    <strong>ID :</strong> <code>tt9362722</code><br>
                    <strong>Query KeyWord :</strong> <mark>Afraid Spider</mark>
                    <strong>Etiquette :</strong> <?php echo $etiquette ?>
                </p>
            </div>
        </li>
    </ul>
</section>
</body>
</html>