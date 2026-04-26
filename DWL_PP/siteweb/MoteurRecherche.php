<?php 

require_once "config/configuration.php";
require_once "service/MovieService.php";
session_start();

$searchResults = [];

$username = $_SESSION['username'] ?? 'Unknown';
$id_user = $_SESSION['id'] ?? 'Unknown';

$api_error = null;

if(isset($_GET["requete"])){
    $query = $_GET["requete"];
    $response = MovieService::searchMotor($query);
    
    // Attention, si message d'erreur on l'intercepte et on la met dans api_error qu'on envoie au html
    if (isset($response['error'])) {
        $api_error = $response['error'];
    } else {
        $searchResults = $response;
    }
}

if(isset($_POST["add_watchlist"])){
    $imdb_id = $_POST["add_watchlist"];
    $metadata = MovieService::getMovieData($imdb_id);
    $ajout = MovieService::addWatchlist($metadata,$id_user);
}

$data = json_decode(file_get_contents('php://input'), true);
if (isset($data['film_ID'])) {
    header('Content-Type: application/json');
    $movieData = MovieService::getMovieData($data['film_ID']);
    echo json_encode($movieData);
    exit; // TRÈS IMPORTANT : on arrête tout ici !
}
if (isset($_POST["connexion-deconnexion"])){
    if ($username != "Unknown") {
        $conneted = "Your are logged out";
        session_unset();
        session_destroy();
        header("Location: MoteurRecherche.php");
        exit;
    }
    else {
        header("Location: Login.php");
        exit;
    }
}
require_once "view/affichage_Search.php"

?>