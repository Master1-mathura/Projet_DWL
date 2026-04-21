<?php 

require_once "config/configuration.php";
require_once "service/MovieService.php";

$searchResults = [];

if(isset($_POST["query"])){
    $query = $_POST["query"];
    $res = MovieService::searchMotor($query);

    $searchResults = json_decode($res, true); # on decode le json recu de flask
}
if(isset($_POST["add_watchlist"])){
    $imdb_id = $_POST["add_watchlist"];
    $metadata = MovieService::getMovieData($imdb_id);
    $ajout = MovieService::addWatchlist($metadata);
}

$data = json_decode(file_get_contents('php://input'), true);
if (isset($data['film_ID'])) {
    header('Content-Type: application/json');
    echo  MovieService::getMovieData($data['film_ID']);
    exit; // TRÈS IMPORTANT : on arrête tout ici !
}
require_once "view/affichage_Search.php"

?>