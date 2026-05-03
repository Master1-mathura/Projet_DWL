<?php

class MovieService
{
    const CURRENT_USER_ID = 1;
    private static function appelAPI ($url, $methode = 'GET', $donnees = null)
    {
        $options = [
            "http" => [
                "method" => $methode,
                "header" => "Content-Type: application/json",
                "ignore_errors" => true 
            ]
        ];
        if ($donnees !== null) {
            $options['http']['content'] = is_string($donnees) ? $donnees : json_encode($donnees);
        }
        $contexte = stream_context_create($options);
        $reponse = @file_get_contents($url, false, $contexte);

        if ($reponse === false) {
            return ["error" => "Serveur API indisponible."];
        }

        $donnees_decodees = json_decode($reponse, true);
        return $donnees_decodees !== null ? $donnees_decodees : [];
    }

    public static function searchMotor($query){
        $url = API_BASE_URL . "/search?q=" . urlencode($query);
        $response = self::appelAPI($url);
        // attention lui on le laisse passer tel qu'il est pour afficher "model is loading"
        return $response; 
    }

    public static function getWatchlist($user_id)
    {
        $url = API_BASE_URL . "/watchlist" . "/" . $user_id;
        $response = self::appelAPI($url);
        return isset($response['error']) ? [] : $response;
    }

    public static function addWatchlist($metadata, $user_id){
        $url = API_BASE_URL . "/watchlist";
        $donnees = is_string($metadata) ? json_decode($metadata, true) : $metadata;
        $donnees['user_id'] = $user_id;

        return self::appelAPI($url, 'POST', $donnees);
    }

    public static function getMovieData($filmID){
        $url = API_BASE_URL . "/movies" . "/" . $filmID;
        return self::appelAPI($url);
    }

    public static function deleteMovieWL($filmID, $user_id){
        $url = API_BASE_URL . "/watchlist"  . "/" . $user_id . "/" . $filmID ;
        return self::appelAPI($url, 'DELETE');
    }

    public static function updateEtat($filmID, $nv_etat, $user_id){
        $url = API_BASE_URL . "/watchlist"  . "/" .  $user_id . "/" . $filmID ;
        return self::appelAPI($url, 'PUT', ["etat" => $nv_etat]);
    }

    public static function creerCompte($data){
        $url = API_BASE_URL . "/compte";
        return self::appelAPI($url, 'POST', $data);
    }

    public static function connexion($data){
        $url = API_BASE_URL . "/connexion";
        return self::appelAPI($url, 'POST', $data);
    }

    public static function updateProfile($data){
        $url = API_BASE_URL . "/compte" . "/" . $data["id"];
        return self::appelAPI($url, 'PUT', $data);
    }

    public static function deleteProfile($id_user){
        $url = API_BASE_URL . "/compte" . "/" . $id_user;
        return self::appelAPI($url, 'DELETE');
    }
    public static function updateUserSettings($user_id, $theme, $blurred) {
        $url = API_BASE_URL . "/usersettings" . "/" . $user_id;
        return self::appelAPI($url, 'PUT', ["theme" => $theme, "blur_effect" => $blurred]);
    }
    public static function getUserSettings($user_id) {
        $url = API_BASE_URL . "/usersettings" . "/" . $user_id;
        return self::appelAPI($url);
    }
}
?>