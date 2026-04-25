<?php
require_once "config/configuration.php";
require_once "service/MovieService.php";

session_start();

if(isset($_POST["connexion"])){
    $data = [
        "username" => $_POST["username"],
        "password" => $_POST["password"]
    ];
    $result = MovieService::connexion($data);
    if(isset($result['error'])){
        $error = $result['error'];
    }
    if(isset($result['message'])){
        $message = $result['message'];
        $_SESSION['username'] = $data['username'];
        $_SESSION['id'] = $result['data']['id'];
    }
}

require_once "view/affichage_Login.php";
?>