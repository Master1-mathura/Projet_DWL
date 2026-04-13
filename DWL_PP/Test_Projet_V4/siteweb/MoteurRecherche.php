<?php 

require_once "config/configuration.php";
require_once "service/MovieService.php";

$url = API_BASE_URL . "/search";


if(isset($_POST["query"])){
    $query = $_POST["query"];
    $res = MovieService::searchMotor($query);
    echo "<p>" . $res . "</p>";
}

$liste = MovieService::getAll();
require_once "view/affichage_Search.php"

?>