<?php 
require_once "config/configuration.php";
$url = API_BASE_URL . "/";

$response = file_get_contents($url);

require_once "view/affichage_DWL.php";
?>