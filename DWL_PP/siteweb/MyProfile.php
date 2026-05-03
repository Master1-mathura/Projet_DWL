<?php 
require_once "config/configuration.php";
require_once "service/MovieService.php";


session_start();
$username = $_SESSION['username'] ?? 'Unknown';

if ($_SESSION['username'] == "Unknown") {
    header("Location: Login.php");
    exit;
}

$id_user = $_SESSION['id'];

$theme = $_SESSION['theme'];
$isBlurred = $_SESSION['isBlurred'];

if(isset($_POST['DarkMode'])) {
    $response = MovieService::updateUserSettings($id_user, "dark", $isBlurred);
    if(isset($response["message"])) {
        $_SESSION['theme'] = "dark";
        $theme = "dark";
    }
}

if(isset($_POST['LightMode'])) {
    $response = MovieService::updateUserSettings($id_user, "light", $isBlurred);
    if(isset($response["message"])) {
        $_SESSION['theme'] = "light";
        $theme = "light";
    }
}

if(isset($_POST['cocherBlurPoster'])) {
    if(isset($_POST['blurPoster'])) {
        $isBlurred = "on";
    }
    else {
        $isBlurred = "off";
    }

    MovieService::updateUserSettings($id_user, $theme, $isBlurred);
    $_SESSION['isBlurred'] = $isBlurred;


}
$ma_watchlist = MovieService::getWatchlist($id_user);
$nombre_de_films = count($ma_watchlist);


require_once "view/affichage_myprofile.php";
?>