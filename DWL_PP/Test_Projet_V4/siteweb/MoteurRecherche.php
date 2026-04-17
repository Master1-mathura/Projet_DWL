<?php 

require_once "config/configuration.php";
require_once "service/MovieService.php";

$searchResults = [];

if(isset($_POST["query"])){
    $query = $_POST["query"];
    $res = MovieService::searchMotor($query);

    $searchResults = json_decode($res, true); # on decode le json recu de flask
}

$liste = MovieService::getAll();
require_once "view/affichage_Search.php"

?>