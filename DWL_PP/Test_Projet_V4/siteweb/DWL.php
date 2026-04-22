<?php 
require_once "config/configuration.php";
require_once "service/MovieService.php";

$url = API_BASE_URL . "/";

$response = file_get_contents($url);

$watchlist = MovieService::getAll();
require_once "view/affichage_DWL.php";
?>