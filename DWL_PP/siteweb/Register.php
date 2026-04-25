<?php
require_once "config/configuration.php";
require_once "service/MovieService.php";

if(isset($_POST["register"])){
    $data = [
        "username" => $_POST["username"],
        "password" => $_POST["password"]
    ];
    $result = MovieService::creerCompte($data);
    if(isset($result['error'])){
        $error = $result['error'];
    }
    if(isset($result['message'])){
        $message = $result['message'];
    }
}

require_once "view/affichage_Register.php";
?>