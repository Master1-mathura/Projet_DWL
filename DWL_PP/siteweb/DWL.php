<?php 
require_once "config/configuration.php";
require_once "service/MovieService.php";

if (isset($_POST["delete_id"])) {
    $id_a_supprimer = $_POST["delete_id"];
    MovieService::deleteMovieWL($id_a_supprimer); 
        header("Location: DWL.php");
    exit;
}


$url = API_BASE_URL . "/";

$response = file_get_contents($url);

$watchlist = MovieService::getWatchlist();
require_once "view/affichage_DWL.php";
?>