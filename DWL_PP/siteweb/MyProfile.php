<?php 
require_once "config/configuration.php";
require_once "service/MovieService.php";


session_start();
$username = $_SESSION['username'] ?? 'Unknown';

if ($username === 'Unknown') {
    header("Location: Login.php");
    exit;
}

$id_user = $_SESSION['id'] ?? null;
$theme = $_SESSION['theme'] ?? 'dark';
$isBlurred = $_SESSION['isBlurred'] ?? 'off';

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
$data = json_decode(file_get_contents('php://input'), true);

if (isset($data['badgeName'])) {
    header('Content-Type: application/json');
    $response = MovieService::saveUserBadge($id_user, $data['badgeName']);
    echo json_encode($response);
    exit;
}
$tous_les_badges = MovieService::getAllBadges();
$badge_debloques = MovieService::getUserBadges($id_user);

if (!is_array($badge_debloques) || isset($badge_debloques['error'])) {
    $badge_debloques = [];
}
if (!is_array($tous_les_badges) || isset($tous_les_badges['error'])) {
    $tous_les_badges = [];
}

$ma_watchlist = MovieService::getWatchlist($id_user);
$survecu = 0;
$abandonne = 0;
foreach ($ma_watchlist as $film){
    if ($film["etat"] == "Survécu"){
        $survecu++;
    }
    elseif ($film["etat"] == "Abandon"){
        $abandonne++;
    }
}

$nombre_de_films = count($ma_watchlist);

require_once "view/affichage_myprofile.php";
?>