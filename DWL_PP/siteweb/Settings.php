<?php
require_once "config/configuration.php";
require_once "service/MovieService.php";


session_start();
$username = $_SESSION['username'] ?? 'Unknown';
if ($username == "Unknown") {
    header("Location: Login.php");
    exit;
}

$username = $_SESSION['username'];
$id_user = $_SESSION['id'];
$theme = $_SESSION['theme'];


$ma_watchlist = MovieService::getWatchlist($id_user);


if(isset($_POST['update_profile'])){
    $data = [
        "id" => $id_user,
        "username" => $_POST['new_username'],
        'old_mdp' => $_POST['old_password'],
        "mdp" => $_POST['new_password']

    ];
    $data = MovieService::updateProfile($data);
    if(isset($data['error'])){
        $error = $data['error'];
    }
    if(isset($data['message'])){
        if (isset($_POST['new_username']) && !empty($_POST['new_username'])) {
            $username = $_POST['new_username'];
            $_SESSION['username'] = $username;
        }
        $message = $data['message'];
    }

}

if(isset($_POST["delete_profile"])){
    $reponse = MovieService::deleteProfile($id_user);
    if(isset($reponse['error'])){
        $error = $reponse['error'];
    }
    if(isset($reponse['message'])){
        $message = $reponse['message'];
        session_destroy();
        header("Location: Login.php");
        exit();
    }
}
$nombre_de_films = count($ma_watchlist);
require_once "view/affichage_settings.php";
?>