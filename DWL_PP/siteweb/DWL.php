<?php 
require_once "config/configuration.php";
require_once "service/MovieService.php";
session_start();

$username = $_SESSION['username'] ?? 'Unknown';
if ($username == "Unknown") {
    header("Location: Login.php");
    exit;
}
$id_user = $_SESSION['id'];

if (isset($_POST["delete_id"])) {
    $id_a_supprimer = $_POST["delete_id"];
    MovieService::deleteMovieWL($id_a_supprimer, $id_user); 
    header("Location: DWL.php");
    exit;
}

if (isset($_POST["update_id"]) && isset($_POST["nv_etat"]) && !empty($_POST["update_id"])) {
    MovieService::updateEtat($_POST["update_id"], $_POST["nv_etat"], $id_user);
    header("Location: DWL.php");
    exit;
}

$watchlist = MovieService::getWatchlist($id_user);
require_once "view/affichage_DWL.php";
?>